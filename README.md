# AOC 2024
Another year, another advent of code. It's a very busy time right now, so I won't be doing anything fancy, just doing the usual on Python. As usual I will be trying to limit myself to the standard set of libraries.

## Day 1
EZ GG. Just some list manipulation and trivial use of built in list manipulation functions.

## Day 2
Part 1 was pretty easy, but then fell into the trap of premature optimisation. Part 2 complexity is O(5n) when brute forcing. It's trivial.

Anyway, I did try to make it a bit more efficient.

## Day 3
REGEXES BABBAY. Nice easy one.

## Day 4
Why did I decide to rotate the arrays, this is so ugly, urgh. It works though

## Day 5
Sets and recursion, I like this solution. Clean, precise, good.

I'm very surprised that almost everything worked first time without tweaking. I was sure my inserts were going to need more index tweaking. I think, depending on my input set the recursion could go endlessly, but, unlikely, maybe.

## Day 6
I think this was the first really challenging one, you need to think some thonks to figure this one out. My first approach was not good (check `day06_derp.py`), essentially I was only searching for obstacles which would get you in a loop by entering you into an already travelled path. This was pretty close to the right answer (1611 vs 1705) all things considered, and was of course, very fast.

The actual solution is not too bad. I had a brief error where I assumed I can't place any obstacles in line of sight of the starting position of the guard, but happily that was not the case.

## Day 7
I started by trying something fancy but half arsing it, then seeing brute forcing it is reasonaly quick if done well, I had a solution which executed in 33s. After finding a bug making the search tree unnecesarily big, that was brought down to 8s.

Then while in the shower tonight I suddenly realised how to do the fancy thing, and, well, here we are. Speedy!

## Day 8
I had a vague idea what part 2 would be, but it was easier than expected. Nice little solution in the end. I got stuck for a few minutes not grokking that I have to include antenna positions as nodes in part 2.

## Day 9
No big comments, was pretty easy, didn't feel like doing any kind of optimisation

## Day 10
Started very late, lots of personal life got in the way. Humourously I accidentally solved P2 while writing P1, not realising P1 only asked for number of ends and not paths. Could probably halve the execution time by combining the two searches with some good handling of the data being passed around, but I am le tired.

## Day 11
More recursion! Spent some time debugging to find a rogue +1 I kept glossing over. Quick enough for P1, dog slow for P2. Rethought it a bit and the solution is as you see it.