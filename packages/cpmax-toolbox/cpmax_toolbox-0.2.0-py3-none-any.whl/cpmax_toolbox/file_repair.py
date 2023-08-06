import pandas as pd
from pathlib import Path
import csv
import typing
import datetime
import json
import warnings


def parse_path(path_str: str) -> Path:
    p = Path(path_str)
    if not p.is_file():
        raise ValueError("Is not a file")

    if not p.exists():
        raise FileNotFoundError("File not found")
    return p


def detect_file_type(path_to_file: Path) -> str:
    """TODO sqlite Export integrieren -> unlocker mit bundlen (wie sieht das mit pypi aus?)"""
    dialect = None

    with open(path_to_file) as f:
        for i, line in enumerate(f.readlines()):
            try:
                dialect = csv.Sniffer().sniff(line, delimiters=",\t")
                break
            except Exception:
                pass

            if i == 500:
                raise ValueError("Could not find delimiter!")

        f.seek(0)

        if dialect is None:
            raise ValueError("Could not find delimiter!")

        anz_parts = []
        for i, line in enumerate(f.readlines()):
            anz_parts.append(len(line.split(dialect.delimiter)))
            if i == 500:
                break
        f.seek(0)

        anz_cols = sorted(anz_parts)[len(anz_parts) // 2]
        i = 0
        for i, line in enumerate(f.readlines()):
            if len(line.split(dialect.delimiter)) == anz_cols:
                break
        f.seek(0)
        df = pd.read_csv(f, dialect=dialect, skiprows=i, nrows=500)  # type: ignore

    set_cols = set(df.columns)

    if (
        set_cols
        == set(
            [
                "ID",
                "Measurement_ID",
                "AxialSignal",
                "RadialSignal",
                "TorsionalSignal",
                "RotationTrigger",
                "WindSpeed",
            ]
        )
        and i == 0
    ):
        return "sqlite_export"

    if set_cols == set(["millis", "ax", "ay", "az", "trig"]) and i == 2:
        return "old_nanovib_recording"

    if set_cols == set(["Axial", "Radial", "Torsional", "Trigger"]) and i == 3:
        return "new_nanovib_recording"

    raise ValueError(
        f"Unknown format, cols are {set_cols} and header is {i} lines long"
    )


def repair_file(p: typing.Union[Path, str]) -> Path:
    """
    TODO test with broken files -> create broken files

    repair broken file and return viba ready file.
    possible types:
        sqlite_export -> fs?
        old_nanovib_recording
        new_nanovib_recording

        possible errors:
            missing linebreak -> repair/ignore?
            incomplete write
            encoding problem?


    """
    if isinstance(p, str):
        p = parse_path(p)

    if not p.is_absolute():
        p = p.absolute()

    file_type = detect_file_type(p)

    """ if parted measurmeent -> combine """
    if p.stem.endswith("0001"):
        p_combined = p.parent / (p.stem[:-4] + "_combined" + p.suffix)
        p_part = p
        with open(p_combined, "w") as fw:
            while p_part.exists():
                with open(p_part) as fr:
                    fw.write(fr.read())

                i = int(p_part.stem[-4:])
                i += 1
                p_part = p_part.parent / (
                    p_part.stem[:-4] + str(i).zfill(4) + p_part.suffix
                )
        p = p_combined
    p_new = p.parent / (p.stem + "_fix.txt")

    dt_line = "None"

    if file_type == "sqlite_export":
        df = pd.read_csv(p, encoding_errors="replace", on_bad_lines="skip")

        """ get mid (from user input) """
        m_ids = set(df["Measurement_ID"])
        if len(m_ids) > 1:
            choice = ""
            while not choice:
                try:
                    m_id_str = ", ".join([str(elem) for elem in sorted(list(m_ids))])
                    choice = int(input(f"Measurement_ID ({m_id_str}) ?: "))
                except ValueError:
                    choice = ""
                choice = "" if choice not in m_ids else choice
            df = df[df["Measurement_ID"] == choice]
        df = df[
            ["AxialSignal", "RadialSignal", "TorsionalSignal", "RotationTrigger"]
        ].rename(
            columns={
                "AxialSignal": "Axial",
                "RadialSignal": "Radial",
                "TorsionalSignal": "Torsional",
                "RotationTrigger": "Trigger",
            }
        )

        """ get fs """
        fs = 0
        while fs == 0:
            try:
                fs = int(input("Abtastrate in Hz: "))
                if (fs < 1) or (fs > 5000):
                    fs = 0
            except ValueError:
                fs = 0

    elif file_type == "old_nanovib_recording":
        with open(p) as f:
            dt_line = f.readline().strip()
            settings_line = f.readline()
            df = pd.read_csv(f, encoding_errors="replace", on_bad_lines="skip")

        translation_dict = {"ay": "Axial", "ax": "Radial", "trig": "Trigger"}

        if "gz" in df.columns:
            translation_dict["gz"] = "Torsional"
        else:
            translation_dict["az"] = "Torsional"

        for ax_orig, ax_new in translation_dict.items():
            df[ax_new] = 1000 * df[ax_orig]
        df = df[["Axial", "Radial", "Torsional", "Trigger"]]
        try:
            settings = json.loads(settings_line)
            fs = int(1000 / (1 + settings["sensor"]["srd"]))
        except (json.JSONDecodeError, KeyError):
            warnings.warn(
                "can't read settings json line of old nanovib recording using default samplerate of 500Hz"
            )
            fs = 500

    elif file_type == "new_nanovib_recording":
        with open(p) as f:
            fs_line = f.readline().strip()
            dt_line = f.readline().strip()
            f.readline()
            df = pd.read_csv(
                f, sep="\t", encoding_errors="replace", on_bad_lines="skip"
            )

        fs = int(fs_line.split("\t")[-1].split(" ")[0])
        dt_line = " ".join(dt_line.split("\t")[1:])

    else:
        raise ValueError(f"got Unknown Filetype: {file_type}")

    dt = datetime.datetime.min
    for dt_format in ["%d.%m.%Y %H:%M:%S", "%Y%m%d_%H%M%S"]:
        try:
            dt = datetime.datetime.strptime(dt_line, dt_format)
        except ValueError:
            pass

    if dt.year == datetime.datetime.min:
        if file_type != "sqlite_export":
            warnings.warn(f"Date not recognised ({dt_line}), current dt used")
        dt = datetime.datetime.now()

    """ TODO Korrektur Achsen ermöglichen, wenn Torsional auf falscher Achse """

    """ check and correction possibility of sample rate"""
    choice = ""
    choice = "y"
    while choice not in ("y", "j", "n"):
        choice = input(f"Samplerate {fs} Hz korrekt? (y/n): ")
        if len(choice) > 0:
            choice = choice.lower()[0]

    if choice == "n":
        fs = 0
        while fs < 1:
            try:
                fs = int(input("Korrekur Samplerate [Hz]: "))
            except ValueError:
                fs = 0

    
    """ check and correction possibility of scaling """
    # df.rename(columns= {"Axial":"Torsional", "Torsional":"Axial"}, inplace=True)
    ax_mean = df["Axial"].mean()
    rad_mean = df["Radial"].mean()
    tor_mean = df["Torsional"].mean()

    geo_mean = (ax_mean**2 + rad_mean**2 + tor_mean**2)**(1/2)
    tor_ratio = abs(tor_mean) / geo_mean

    if tor_ratio < 0.9:
        ax_ratio = abs(ax_mean) / geo_mean
        rad_ratio = abs(rad_mean) / geo_mean
        fitting_ax = "Axial" if ax_ratio > rad_ratio else "Radial"

        print(f"Torsionsachse zeigt nicht nach unten, stattdessen wird {fitting_ax} genutzt.")
        all_axes = {"Axial", "Radial", "Torsional"}

        nfa = list(all_axes - set([fitting_ax]))
        choice_1 = (nfa[0].lower()[0], nfa[0], df[nfa[0]].mean())
        choice_2 = (nfa[1].lower()[1], nfa[1], df[nfa[1]].mean())

        choice_1_str = f"{choice_1[1]}: Ø {choice_1[2]:.0f}mm/s²"
        choice_2_str = f"{choice_2[1]}: Ø {choice_2[2]:.0f}mm/s²"

        valid_input = False
        input_value = ""
        while not valid_input:
            input_value = input(f"Welche Achse soll stattdessen für {fitting_ax} genutzt werden? ({nfa[0]} [1], {nfa[1]} [2]): ").lower()[0]
            if input_value in ([c[0].lower() for c in nfa] + ["1","2"]):
                valid_input = True

        if input_value in ("1", "2"):
            i = int(input_value)
            input_value = nfa[i-1].lower()

        print(input_value)
        pass


    meas = (fs, dt, df)
    with open(p_new, "w") as fw:
        fw.write(f"Hardware-Takt:\t{meas[0]} Hz\n")
        date_str = meas[1].strftime("%d.%m.%Y %H:%M:%S")
        fw.write(f"Start der Messung:\t{date_str}\n")
        fw.write("\n")
        meas[2].to_csv(fw, index=False, sep="\t", lineterminator="\n", float_format="%.3f")
        
    return p_new


if __name__ == "__main__":

    path_str_list = [
        # r"C:\Users\j.rose\Documents\ServerSync\GitHub\cpmax-toolbox\tests\test_files\20221025_151509\0001.txt",
        # r"C:\Users\j.rose\Documents\ServerSync\GitHub\cpmax-toolbox\tests\test_files\Berching\output.csv",
        r"C:\Users\j.rose\Documents\ServerSync\GitHub\cpmax-toolbox\tests\test_files\Gardelegen\20221025_103316.csv",
        r"C:\Users\j.rose\Documents\ServerSync\GitHub\cpmax-toolbox\tests\test_files\Gardelegen\20221025_103316.txt",
    ]

    for p_str in path_str_list:
        repair_file(p_str)
