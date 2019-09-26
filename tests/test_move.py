from Move import Move


def test_create_move():
    move = Move(0, 24, 23)
    assert move.from_point == 24
    assert move.to_point == 23
    assert move.colour == 0


def test_get_number_of_positions():
    move = Move(0, 14, 11)
    assert move.get_number_of_positions() == 3

    move = Move(1, 20, 15)
    assert move.get_number_of_positions() == 5


def test_move_to_string():
    move = Move(0, 24, 23)
    assert move.move_to_string() == "BLACK checker moves from point 24 to point 23"

    move = Move(1, 11, 10)
    assert move.move_to_string() == "WHITE checker moves from point 11 to point 10"
