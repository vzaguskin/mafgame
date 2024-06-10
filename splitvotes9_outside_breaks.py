import pygambit as gbt

g = gbt.Game.new_tree(players=["Red", "Black"],
                      title="Sport mafia 9 player stage")

g.append_move(g.root, g.players.chance, ["zero_black", "one_black", "two_black", "three_black"])

g.set_chance_probs(g.root.infoset, [gbt.Rational(10, 56), gbt.Rational(30, 56), gbt.Rational(15, 56), gbt.Rational(1, 56)])
for n, node in enumerate(g.root.children):
    if n == 0:
        g.append_move(node, "Black", ["BreakOutside", "Obey"])
    elif n == len(g.root.children) - 1:
        g.append_move(node, "Black", ["Break", "Obey"])
    else:
        g.append_move(node, "Black", ["Break", "BreakOutside", "Obey"])

#handle break case
g.append_move(g.root.children[1].children[0], "Red", ["ClearAll", "Kick1"])
g.append_infoset(g.root.children[2].children[0],
                     g.root.children[1].children[0].infoset)
g.append_infoset(g.root.children[3].children[0],
                     g.root.children[1].children[0].infoset)

#handle break outside case
g.append_move(g.root.children[0].children[0], "Red", ["ClearAll", "Kick1"])
g.append_infoset(g.root.children[1].children[1],
                     g.root.children[0].children[0].infoset)
g.append_infoset(g.root.children[2].children[1],
                     g.root.children[0].children[0].infoset)

#handle obey
g.append_move(g.root.children[0].children[1], "Red", ["Sit", "Standup"])
g.append_infoset(g.root.children[1].children[2],
                     g.root.children[0].children[1].infoset)
g.append_infoset(g.root.children[2].children[2],
                     g.root.children[0].children[1].infoset)
g.append_infoset(g.root.children[3].children[1],
                     g.root.children[0].children[1].infoset)

#"zero_black "BreakOutside" "ClearAll"/ "Kick1""
g.set_outcome(g.root.children[0].children[0].children[0], g.add_outcome([0, 1]))
g.set_outcome(g.root.children[0].children[0].children[1], g.add_outcome([1/6, 5/6])) #5 players 2 black 1 checked red

#"zero_black "Obey" "Sit"/ "Standup""
g.set_outcome(g.root.children[0].children[1].children[0], g.add_outcome([0.2, 0.8]))
g.set_outcome(g.root.children[0].children[1].children[1], g.add_outcome([0, 1]))

#"one_black "Break" "ClearAll"/ "Kick1""
g.set_outcome(g.root.children[1].children[0].children[0], g.add_outcome([0, 1]))
g.set_outcome(g.root.children[1].children[0].children[1], g.add_outcome([0.3, 0.7])) #7 total 2 black 2 checked red

#"one_black "BreakOutside" "ClearAll"/ "Kick1""
g.set_outcome(g.root.children[1].children[1].children[0], g.add_outcome([0, 1]))
g.set_outcome(g.root.children[1].children[1].children[1], g.add_outcome([0, 1]))

#"one_black "Obey" "Sit"/ "Standup""
g.set_outcome(g.root.children[1].children[2].children[0], g.add_outcome([0, 1]))
g.set_outcome(g.root.children[1].children[2].children[1], g.add_outcome([8 / 35, 27 / 35])) # 5 total 2 black 0 checked red

#"two_black "Break" "ClearAll"/ "Kick1"", assuming red player kicked out ad break
g.set_outcome(g.root.children[2].children[0].children[0], g.add_outcome([1/3, 2/3]))# end up with 3 players guessing game
g.set_outcome(g.root.children[2].children[0].children[1], g.add_outcome([0, 1]))

#"two_black "BreakOutside" "ClearAll"/ "Kick1""
g.set_outcome(g.root.children[2].children[1].children[0], g.add_outcome([1, 0]))
g.set_outcome(g.root.children[2].children[1].children[1], g.add_outcome([0, 1]))

#"two_black "Obey" "Sit"/ "Standup""
g.set_outcome(g.root.children[2].children[2].children[0], g.add_outcome([0, 1]))
g.set_outcome(g.root.children[2].children[2].children[1], g.add_outcome([7/15, 8/15]))  # 1 black 4 red no checked red

#"three_black "Break" "ClearAll"/ "Kick1""
g.set_outcome(g.root.children[3].children[0].children[0], g.add_outcome([1, 0]))
g.set_outcome(g.root.children[3].children[0].children[1], g.add_outcome([0, 1]))

#"three_black "Obey" "Sit"/ "Standup""
g.set_outcome(g.root.children[3].children[1].children[0], g.add_outcome([0, 1]))
g.set_outcome(g.root.children[3].children[1].children[1], g.add_outcome([1, 0]))



for c in g.root.children:
    print(c.prior_action.label)
    for c2 in c.children:
        print("\t", c2.prior_action.label)
        for c3 in c2.children:
            print("\t\t", c3.prior_action.label)


result = gbt.nash.lcp_solve(g)
eqm = result.equilibria[0]

print("Red:")
for (iset, rat) in eqm["Red"].mixed_actions():
    print(iset.members[0].prior_action.label, [(r[0].label, float(r[1])) for r in rat])

print("payoff", float(eqm.payoff("Red")))

print("Black:")
for nb, (iset, rat) in enumerate(eqm["Black"].mixed_actions()):
    print(f"{nb} black in split: ", [(r[0].label, float(r[1])) for r in rat])
print("payoff", float(eqm.payoff("Black")))




