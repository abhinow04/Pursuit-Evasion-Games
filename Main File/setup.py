import numpy as np
import gogoal2
import ev3_send_val
import assign
import initialise_game

class initialiser:
    def __init__(self, p_pos, e_pos):
        self.p0 = p_pos[0]
        self.p1 = p_pos[1]
        self.e = e_pos
        self.tol = 0.08
        self.p0s = 0
        self.p1s = 0
        self.es = 0
        self.p0_move = [0,0,0]
        self.p1_move = [0,0,0]
        self.e_move = [0,0,0]

    def set(self, bot):
        self.p, self.ei = initialise_game.get_positions()
        self.p0i, self.p1i = self.p
        print(self.p0i)
        if bot == "p0":
            print(abs(np.linalg.norm(self.p0 - self.p0i)))
            if (self.p0s == 0 and abs(np.linalg.norm(self.p0 - self.p0i)) > self.tol):
                print(self.p0i)
                print(self.p0)
                # Correct: move to target position, not current
                self.p0_move = gogoal2.OmniRobot(np.array(self.p0i), 0).move_to_target(self.p0)
                print("moto:", self.p0_move)
            else:
                self.p0_move = [0,0,0]
                self.p0s = 1
        elif bot == "p1":
            if (self.p1s == 0 and abs(np.linalg.norm(self.p1 - self.p1i)) > self.tol):
                self.p1_move = gogoal2.OmniRobot(np.array(self.p1i), 0).move_to_target(self.p1)
            else:
                self.p1_move = [0,0,0]
                self.p1s = 1
        elif bot == "e":
            if (self.es == 0 and abs(np.linalg.norm(self.e - self.ei)) > self.tol):
                self.e_move = gogoal2.OmniRobot(np.array(self.ei), 0).move_to_target(self.e)
            else:
                self.e_move = [0,0,0]
                self.es = 1

    def set_pos(self):
        atmp_lim = 200
        for i in ["p0", "p1", "e"]:
            self.set(i)
            print(self.p0s)
        if (self.p0s == 0 or self.p1s == 0 or self.es == 0):
            attempts = 0
            while (self.p0s == 0 and attempts < atmp_lim):
                if self.p0s == 1:
                    break
                ev3_send_val.send_vel('pursuer0', self.p0_move)
                self.set("p0")
                attempts += 1
            attempts = 0
            while (self.p1s == 0 and attempts < atmp_lim):
                if self.p1s == 1:
                    break
                ev3_send_val.send_vel('pursuer1', self.p1_move)
                self.set("p1")
                attempts += 1
            attempts = 0
            while (self.es == 0 and attempts < atmp_lim):
                if self.es == 1:
                    break
                ev3_send_val.send_vel('evader', self.e_move)
                self.set("e")
                attempts += 1
        else:
            print("------------------------Initialisation Status-------------------------")
            print("Status: All 3 robots set in place, proceeding to Assignment")

def main(args=None):
    N = 2
    n = 2
    m = 1
    v = np.ones(m)
    u = np.ones(n)
    r = 1

    pur_pos = np.random.randn(n, N)
    ev_pos = np.random.randn(m, N)
    print("pursuer position: ", pur_pos, "\n", "evader position: ", ev_pos)

    setup = initialiser(pur_pos, ev_pos)
    setup.set_pos()
    target = np.array([0, 0])

    pur_sp = np.array([[30]] * n)
    eva_sp = np.array([[18]] * m)

    asgn = assign.assignment(pur_pos, ev_pos, target, v, pur_sp, eva_sp)
    asgn.check_win()

main()
