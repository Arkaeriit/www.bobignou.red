---
title: G-forces at Disneyland Paris
date: 2022-05-20 13:57:55
tags:
---

The last time I went to Disneyland Paris, I used my smartphone to record the G-forces during some rides. I used an app called Physics Toolbox Accelerometer to record the acceleration to CSV files. Then, I made a small Python script to filter the data and plot it.

## RC Racer

![RC Racer](https://dlptips.com/wp-content/uploads/RC-Racer-1.jpg)

In this attraction, a cart looking like the RC car in Toys Story rolls back and forth on a U-shaped track. The acceleration measured is the following:

![RC Racer g forces](rc_racer.png)

We can clearly see the moment of minimum acceleration, when the car is on top of the track, about to fall down. We can also see the moments when the car is horizontal, at the bottom of the track when the acceleration is maximal. When first looking at the data, I did not expect to see such a smooth and sine-looking graph.

## Hollywood Tower Hotel

![Hollywood Tower Hotel](https://dlptips.com/wp-content/uploads/Twilight-Zone-Tower-of-Terror-1.jpg)

Hollywood Tower Hotel is an attraction where an elevator cabin drops before climbing swiftly. The acceleration measured is the following:

![Hollywood Tower Hotel g forces](HollywoodTowerHotel.png)

We can see the climbs as sustained high g-forces and the drops as sustained low g-forces. Between series of drops, there is some atmosphere-creating projection, where there is no acceleration one way or another.


## Indiana Jones et le Temple du Péril

![Indiana Jones](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fpbs.twimg.com%2Fmedia%2FCHxj_ENXAAAPLt0.jpg%3Alarge&f=1&nofb=1)

Indiana Jones and the Temple of Doom is a roller coaster with loops and other intense steps. The acceleration measured is the following:

![Indiana Jones g forces](IndianaJones.png)

The first two peaks we see are small drops in the track that are at the beginning of the attraction. Then, the pack of peaks is the rest of the attraction, with a lot of intense turns and loops close to each other. The graph looks a bit messier than the two previous ones and this reflects what we feel when doing this roller coaster.


## Hyperspace Mountain

![Hyperspace Mountain](https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2F4.bp.blogspot.com%2F-u_RQ9OJj1lw%2FWRH7qrzaYFI%2FAAAAAAAAc_o%2FXzyt16O2pJguf4LWLQGyrdA-FWtJag2vACK4B%2Fs1600%2FIMG_2069.jpg&f=1&nofb=1)

Hyperspace Mountain is a (loosely) Star-Wars themed roller coaster. As with Indiana Jones, there are a lot of sharp turns and loops. The acceleration measured is the following:

![Hyperspace Mountain g forces](HyperspaceMountain.png)

We can see a lot of very intense peaks of acceleration. There is also a long pause where a Star Wars-themed light show is presented.

## Big Thunder Mountain

![Big Thunder Mountain](https://media.disneylandparis.com/d4th/fr-fr/images/n017798_2050jan01_big-thunder-mountain_16-9_tcm808-159546.jpg)

Big Thunder Mountain is a softer ride inspired by minecarts. The acceleration measured is the following:

![Big Thunder Mountain g forces](BigThunderMountain.png)

As we can see, the acceleration is way lower than on the previous rides. Furthermore, we can see some long periods with no acceleration, this is where the minecart is being pulled up by chains to gain potential energy.

## Casey Jr. Circus Train

![Casey Jr. Circus Train](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.ytimg.com%2Fvi%2FhbaEVMktdZI%2Fmaxresdefault.jpg&f=1&nofb=1)

Casey Jr. Circus Train is a ride targeted at smaller children. A small train takes the voyagers through a well-landscaped part of the park. The acceleration measured is the following:

![Casey Jr. Circus Train g forces](CircusTrain.png)

As we can see, the acceleration is very low, we can not observe any strong turn.

## Conclusion

The measurements were made with a smartphone in my pocket. As the phone was not secured to the rides, my body and the freedom of movement of the phone might have acted as a mechanical filter which could have changed the graphs a bit. Furthermore, to make the graphs more readable, I used a decimation filter. This is not an issue as all the interesting patterns are at a way lower frequency than what the filters cut.

If you need the raw data for your personal use, send me an e-mail and I will give them to you.

