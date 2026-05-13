from aeropod_x4.physics.aero import drag_force, power_required, reynolds_number


def test_drag_force_basic() -> None:
    d = drag_force(1.225, 10.0, 1.0, 0.1)
    assert abs(d - 6.125) < 1e-6


def test_reynolds_number_basic() -> None:
    re = reynolds_number(1.225, 15.0, 0.1, 1.81e-5)
    assert 100000 < re < 110000


def test_power_required_basic() -> None:
    p = power_required(2.0, 10.0)
    assert p == 20.0
