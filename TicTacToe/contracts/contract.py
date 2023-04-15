from pyteal import *

def tic_tac_toe_approval_program():
    # initialize scratch space
    scratch = ScratchVar(TealType.bytes(10))
    for i in range(10):
        scratch.store(Bytes(i), Int(0))

    # check if game has ended
    def game_ended():
        for i in range(0, 9, 3):
            # check rows
            if scratch.load(Bytes(i)) == scratch.load(Bytes(i+1)) == scratch.load(Bytes(i+2)) and scratch.load(Bytes(i)) != Int(0):
                scratch.store(Bytes(0), Bytes("player won"))
                return True
        for i in range(3):
            # check columns
            if scratch.load(Bytes(i)) == scratch.load(Bytes(i+3)) == scratch.load(Bytes(i+6)) and scratch.load(Bytes(i)) != Int(0):
                scratch.store(Bytes(0), Bytes("player won"))
                return True
        # check diagonals
        if scratch.load(Bytes(0)) == scratch.load(Bytes(4)) == scratch.load(Bytes(8)) and scratch.load(Bytes(0)) != Int(0):
            scratch.store(Bytes(0), Bytes("player won"))
            return True
        if scratch.load(Bytes(2)) == scratch.load(Bytes(4)) == scratch.load(Bytes(6)) and scratch.load(Bytes(2)) != Int(0):
            scratch.store(Bytes(0), Bytes("player won"))
            return True
        # check for draw
        if not any(scratch.load(Bytes(i)) == Int(0) for i in range(9)):
            scratch.store(Bytes(0), Bytes("draw"))
            return True
        return False

    # make a move
    def make_move(position, player):
        if scratch.load(Bytes(position)) != Int(0):
            scratch.store(Bytes(0), Bytes("bad move"))
            return Seq([Return(Int(0))])
        scratch.store(Bytes(position), player)
        if game_ended():
            return Seq([Return(Int(0))])
        for i in range(9):
            if scratch.load(Bytes(i)) == Int(0):
                scratch.store(Bytes(i), Int(2))
                if game_ended():
                    return Seq([Return(Int(0))])
                break
        return Int(1)

    # parse input and make moves
    input = Txn.application_args[0]
    moves = []
    for i in range(8):
        moves.append(input % 10)
        input //= 10
    player = Int(1)
    for i in range(8):
        player = make_move(moves[i], player)
        if type(player) is Return:
            return player
    scratch.store(Bytes(0), Bytes("draw"))
    return Seq([Return(Int(0))])

if __name__ == "__main__":
    print(compileTeal(tic_tac_toe_approval_program(), Mode.Application))
