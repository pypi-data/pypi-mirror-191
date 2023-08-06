import requests
import pytz

import warnings
import json
import threading
import time
from pathlib import Path
import datetime
import typing


def check_dict_scheme(
    d: dict, s: dict, return_bool: bool = False
) -> typing.Union[None, bool]:
    """compares dict d to given scheme s

    e.g.:

    d = {"measurement":{"rpm_min":16.0}}
    s = {"measurement":{"rpm_min":((int,float), 15, 17)}} <-- rpm_min is int or float and lies inbetween 15 and 17
    print(check_dict_scheme(d,s,True))
    >> True

    s = {"measurement":{"rpm_min":((int,float), 17, 18)}} <-- rpm_min is int or float and lies inbetween 17 and 18
    print(check_dict_scheme(d,s,True))
    >> False

    !! caution 16 != 16.0 --> int <-> float --> use
    """
    result = True
    for k, v in d.items():
        if isinstance(v, dict):
            if s[k] and isinstance(s[k], dict):
                if return_bool:
                    result &= bool(check_dict_scheme(d=v, s=s[k], return_bool=True))
                else:
                    check_dict_scheme(v, s[k], False)
            elif not isinstance(s[k], dict):
                if return_bool:
                    result = False
                else:
                    raise ValueError(f"Wrong Scheme! {k} is dict instead of {s[k][0]}")
        else:
            if k not in s.keys():
                if return_bool:
                    return False
                else:
                    raise ValueError(f"{k} not found in scheme, check spelling")
            tuple_comp = s[k]
            if not isinstance(v, tuple_comp[0]):
                if return_bool:
                    return False
                raise ValueError(
                    f"wrong type given for {k}: {type(v)} instead of {tuple_comp[0]}"
                )

            if tuple_comp[0] in (int, float, (int, float)):
                if not (tuple_comp[1] <= v <= tuple_comp[2]):
                    if return_bool:
                        return False
                    raise ValueError(
                        f"Value {k} not within limits ({tuple_comp[1]}, {tuple_comp[2]})"
                    )
            elif tuple_comp[0] in (str,):
                if not (tuple_comp[1] <= len(v) <= tuple_comp[2]):
                    if return_bool:
                        return False
                    raise ValueError(
                        f"length of str {k} not within limits ({tuple_comp[1]}, {tuple_comp[2]})"
                    )
            elif tuple_comp[0] in (bool,):
                pass
            else:
                raise SyntaxError("Cant Validate input")
    if return_bool:
        return result


def wait_until(
    now: typing.Union[float, int],
    delta: typing.Union[float, int],
    ensure_mod: bool = False,
) -> typing.Union[float, int]:
    """
    allows easy regular execution of following code when used as following:
    t = time.time()
    while True:
        t = wait_until(t, 10)
        print(time.time())
    """
    if delta < 0:
        return now

    next_time = now + delta
    while next_time - time.time() > 0:
        time.sleep(0.75 * (next_time - time.time()))

    if ensure_mod:
        next_time = int(next_time)
        while next_time % delta != 0:
            next_time += 1
    return next_time


class NanoVib:
    def __init__(self, ip: str = "192.168.4.1"):
        self._base_url = f"http://{ip}"
        self._ensure_connection()
        self.settings = requests.get(self._base_url + "/settings").json()
        self._settings_scheme = {
            "sensor": {
                "srd": (int, 1, 20),
                "acc_range": (int, 2, 16),
                "bandwidth": (int, 5, 300),
                "calibration": {
                    "sx": (float, 0, 20),
                    "sy": (float, 0, 20),
                    "sz": (float, 0, 20),
                    "bx": (float, -20, 20),
                    "by": (float, -20, 20),
                    "bz": (float, -20, 20),
                },
            },
            "measurement": {
                "max_revolutions": (int, 0, 2e32),
                "rpm_min": (float, 0, 2e32),
                "rpm_max": (float, 0, 2e32),
                "measurement_time": (int, 1000, 300),
                "folder": (str, 3, 254),
                "parted": (bool,),
                "part_size": (int, 1024 * 1024, 2e32),
                "vibA_compatibility": (bool,),
            },
            "system": {"ssid": (str, 3, 254), "password": (str, 8, 254)},
        }
        self._status_scheme = {
            "system": {
                "epoch": (int, 946681200, 4102441200),
            },
            "measurement": {"recording": (bool,)},
        }
        self._update_time()
        self.status = requests.get(self._base_url + "/status").json()
        self.measurements = requests.get(self._base_url + "/measurements").json()
        self.status_thread = threading.Thread(target=self._refresh_status, daemon=True)
        self.status_thread.start()

    def _ensure_connection(self) -> None:
        connected = False
        for i in range(10):
            try:
                self.status = requests.get(self._base_url + "/status", timeout=3).json()
                connected = True
                break
            except Exception as e:
                if i > 3:
                    warnings.warn("Connection takes longer than expected")
                    warnings.warn(str(e))

        if not connected:
            raise ConnectionError(
                "Could not connect to NanoVib, ensure Wifi Connection to NanoVib and try again"
            )

    def _update_time(self) -> None:
        tz = pytz.timezone("Europe/Berlin")
        now = datetime.datetime.now().astimezone(tz)
        offset = now.utcoffset()

        if isinstance(offset, datetime.timedelta):
            offset_seconds = offset.total_seconds()
        else:
            offset_seconds = 0

        patch_dict = {"system": {"epoch": int(now.timestamp() + offset_seconds)}}
        self._update_status(patch_dict)

    def _refresh_status(self) -> None:
        t_next = int(time.time()) + 2
        while True:
            try:
                self.status = requests.get(self._base_url + "/status", timeout=1).json()
            except Exception as e:
                print(e)

            t_next = wait_until(now=t_next, delta=2)

    def _update_status(self, patch_dict) -> None:
        check_dict_scheme(patch_dict, self._status_scheme)
        self.status = requests.patch(
            self._base_url + "/status", data=json.dumps(patch_dict)
        ).json()

    def start_measurement(self, max_revs=None, measurement_time_min=None) -> None:
        settings_dict = {
            "measurement": {
                "max_revolutions": (2e32 if max_revs == None else int(max_revs)),
                "measurement_time": (
                    2e32
                    if measurement_time_min == None
                    else int(measurement_time_min * 60000)
                ),
            }
        }
        self.update_settings(settings_dict)

        patch_dict = {"measurement": {"recording": True}}
        self._update_status(patch_dict)

    def stop_measurement(self) -> None:
        patch_dict = {"measurement": {"recording": False}}
        self._update_status(patch_dict)

    def list_measurements(self) -> typing.Tuple[bool, typing.List[dict]]:
        if self.status["measurement"]["recording"]:
            return (False, self.measurements)
        else:
            return (True, requests.get(self._base_url + "/measurements").json())

    def get_measurement(
        self, project=None, measurement_tag=None, generator=False
    ) -> typing.Generator[Path, None, None]:
        self._ensure_connection()

        """ determine wether live measurement -> live download or project and measurement are given -> only if not measuring """
        """ -> creates meas_base {project}/{measurement_tag}{ext}"""

        if (
            self.status["measurement"]["recording"]
            and not project
            and not measurement_tag
        ):
            meas_base = requests.get(self._base_url + "/measurements").json()[-1][
                "name"
            ]
        else:
            if self.status["measurement"]["recording"]:
                warnings.warn(
                    "measurements active! Download of measurement during another active measurement is not recommended!"
                )
            if project:
                patch_dict = {"measurement": {"folder": project}}
                self.update_settings(patch_dict)
            measurements = requests.get(self._base_url + "/measurements").json()
            found = False
            m = {"name": "", "size": 0}
            for m in measurements:
                if measurement_tag in m["name"]:
                    found = True
                    break
            if not found:
                raise ValueError("Measurement not found")
            meas_base = m["name"]

        if meas_base.endswith(".txt") or meas_base.endswith(".csv"):
            """not parted -> download and if generator yield else return TODO"""
            pass

        else:
            project_name = meas_base.split("/")[1]
            meas_tag = meas_base.split("/")[-1]

            ext = (
                ".txt" if self.settings["measurement"]["vibA_compatibility"] else ".csv"
            )

            dl_path = Path().home() / "Downloads" / project_name
            combined_file = dl_path / (meas_tag + "_combined" + ext)

            last_yielded_at_part = 0

            while True:

                """find highest partnumber of meas"""
                part_found_max = 0
                for p in [p for p in dl_path.iterdir() if meas_tag in p.name]:
                    if p.stem.startswith(meas_tag):
                        try:
                            part_found_max = max(
                                (int(p.stem.split("_")[-1]), part_found_max)
                            )
                        except ValueError:
                            pass

                """ generate url and path of parted file """
                part_url = (
                    self._base_url
                    + meas_base
                    + "/"
                    + str(part_found_max + 1).zfill(4)
                    + ext
                )
                part_file = dl_path / (
                    meas_tag + "_" + str(part_found_max + 1).zfill(4) + ext
                )

                """ get file from device """
                try:
                    resp = requests.get(part_url, timeout=60)
                except Exception as e:
                    print(e)
                    time.sleep(5)
                    continue

                if resp.status_code == 200:
                    with open(part_file, "wb") as f:
                        f.write(resp.content)

                    with open(combined_file, "ab") as f:
                        f.write(resp.content)

                if resp.status_code == 409:
                    if last_yielded_at_part != part_found_max:
                        last_yielded_at_part = part_found_max
                        t0 = time.time()
                        yield combined_file
                        wait_until(now=t0, delta=5)

                if resp.status_code == 404:
                    if last_yielded_at_part != part_found_max:
                        yield combined_file
                    break

    def update_settings(self, patch_dict: dict, check_scheme: bool = True):
        self._ensure_connection()
        if not check_scheme:
            check_dict_scheme(patch_dict, self._settings_scheme)
        settings_old = self.settings
        resp = requests.patch(
            self._base_url + "/settings", data=json.dumps(patch_dict), timeout=1
        )
        if resp.status_code != 200:
            warnings.warn(
                f"Status Code 200 expected, got {resp.status_code} - {resp.text}"
            )
        else:
            self.settings = resp.json()

        if (
            settings_old["measurement"]["folder"]
            != self.settings["measurement"]["folder"]
        ):
            self.measurements = requests.get(self._base_url + "/measurements").json()


if __name__ == "__main__":
    nano = NanoVib()

    nano.start_measurement(measurement_time_min=20)

    for updated_file in nano.get_measurement(generator=True):
        print(updated_file.stat().st_size)

    nano.stop_measurement()
