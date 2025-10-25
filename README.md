# Run Poster

After a long break of several years, I finally returned to our art school and enrolled in the course [graphic design and illustrations](https://www.heist-op-den-berg.be/grafisch-ontwerp-en-illustratie). One of the year-projects required me to design a poster that presented statistical information related to a topic of my choice. I decided to use my Strava statistics for this project.

While I could have manually created the poster, I saw an opportunity to integrate computer graphics and math to produce a visually appealing visualization of several of my statistics.

This repository and README document my journey throughout the year, beginning with downloading my statistics from Strava, setting up the canvas, and exploring uncharted mathematical concepts, using SVG as a format.

## Minimal Survival Commands

Want to run this yourself on your own Strava data? First [download your personal Strava data](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export) and unpack it in a checkout of this repository in a folder called `strava`. Next:

```console
% pip install requirements.txt
% python -m runposter strava/activities.csv > canvas.svg
```

This will produce a poster called `canvas.svg` based on this years activities.

## My Journal

### October 25: Spiraling Circles

In the end, I intend to print the poster on an A0 format. Therefore, I selected a canvas size of `width=841, height=1189` and started working on my initial design. This design features a circular representation of a run, with the runs arranged along an [Archimedean spiral](https://en.wikipedia.org/wiki/Archimedean_spiral). The design also implements fixed distances between the consecutive circles.

Given an angle $\theta$ and a spiralling factor $a$, the cartesian positions are defined as:

$$
x = a\ \theta\ cos(\theta)\\
y = a\ \theta\ sin(\theta)
$$

Credits to [Cye Waldman](https://math.stackexchange.com/users/424641/cye-waldman) for his answer on [Math StackExchange](https://math.stackexchange.com/a/2216736) that explains how, given a fixed in-between distance $\Delta s$, we can compute the next $\theta_{n}$.

$$
\Delta \theta = \frac{\Delta s}{\sqrt{1+\theta_{n-1}^2}}\\
\theta_{n} = \theta_{n-1} + \Delta \theta
$$

![spiraling canvas](assets/canvas.20251025.svg)
