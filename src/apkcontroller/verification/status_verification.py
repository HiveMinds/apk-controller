"""Performs verifications on the status of the phone."""
from typing import TYPE_CHECKING, Dict, List, Tuple

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.apkcontroller.helper import (
    export_screen_data,
    get_screen_as_dict,
    is_expected_screen,
)
from src.apkcontroller.script_orientation import get_expected_screens

# pylint: disable=R0801
if TYPE_CHECKING:
    from src.apkcontroller.org_torproject_android.V16_6_3_RC_1.Apk_script import (
        Apk_script,
    )
    from src.apkcontroller.Screen import Screen
else:
    Screen = object
    Apk_script = object


@typechecked
def can_proceed(
    dev: AutomatorDevice,
    expected_screennames: List[int],
    retry: bool,
    script: Apk_script,
) -> Tuple[bool, int]:
    """Checks whether the screen is expected, raises an error if not.

    And it returns the current screen number.
    """
    # get current screen dict.
    unpacked_screen_dict: Dict = get_screen_as_dict(
        dev=dev,
        unpack=True,
        screen_dict={},
        reload=False,
    )

    # verify current_screen in next_screens.
    is_expected, screen_nr = current_screen_is_expected(
        dev=dev,
        expected_screennames=expected_screennames,
        retry=retry,
        script_graph=script.script_graph,
        unpacked_screen_dict=unpacked_screen_dict,
    )

    # end_screens = get end_screens()
    if not is_expected:
        # Export the actual screen, screen data and expected screens in
        # specific error log folder.
        export_screen_data(
            dev=dev,
            screen_dict=unpacked_screen_dict,
            script_description=script.script_description,
            overwrite=True,
            subdir="error",
        )
        raise ReferenceError(
            f"Error, the expected screen was not found in:{screen_nr}. "
            + f"Searched for:{expected_screennames}. The accompanying screen "
            + "and xml can be found in:src/apkcontroller/<package_name>/<app_"
            + f'version>/error/{script.script_description["screen_nr"]}.json'
        )
    return is_expected, screen_nr


@typechecked
def current_screen_is_expected(
    dev: AutomatorDevice,
    expected_screennames: List[int],
    retry: bool,
    script_graph: nx.DiGraph,
    unpacked_screen_dict: Dict,
) -> Tuple[bool, int]:
    """Determines whether the current screen is one of the expected screens."""
    expected_screens: List[Screen] = get_expected_screens(
        expected_screennames, script_graph
    )
    for expected_screen in expected_screens:
        if is_expected_screen(
            dev=dev,
            expected_screen=expected_screen,
            retry=retry,
            unpacked_screen_dict=unpacked_screen_dict,
        ):

            return (
                True,
                int(str(expected_screen.script_description["screen_nr"])),
            )
    return (False, -1)