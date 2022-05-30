# Closest-Pair-Randomized-Algorithm
A randomized algorithm to compute the closest distance of point pairs

The algorithmic complexity is $O(n)$

Following these steps:

Denote $\delta^* $ as the minimum distance of all point pairs

1. Randomly select $\lfloor\sqrt{n}\rfloor$ points from set $S (|S|=n)$ as subset $T$;
2. Calculate the minimum distance of point pairs $\delta$ in subset $T$;
3. Draw grids which side length is $\delta$ to cover all points in $S$;
4. Store the points that belong to a grid in a hash map;
5. Find the grid which has the max points, if it exceeds $\sqrt{n}$, divide the grid into quarters until it less than $\sqrt{n}$;
6. Find the minimun distance $\delta$ of point pair in the grid which has the max points;
7. Redraw grids using the side length $\delta$ ($\delta \geq \delta^* $);
8. The closest pair must in one of four $2\delta \times 2\delta$ grids, which show as below:
![](https://user-images.githubusercontent.com/75724651/170980202-a30f5d49-e650-4db5-b5d9-7407ba1ce95f.png)
9. Find the closest pair in these grids.
