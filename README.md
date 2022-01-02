# geo_project
GeoGuessr Image-Based Location Retrieval

**Intro**

GeoGuessr is a game that drops players you in a random Google Street View location, anywhere in the world. The objective is to determine where you are. If you guess the exact location you'll earn 5000 points and if you guess the opposite side of the world you'll earn 0 points. There are many different modes of playing. This program is specifically for the "No Moving, Panning, or Zooming" mode where you have to guess the location based on a single image. There are also many different maps which have varying focuses such as region or type of location. This program works specifically with the "A Diverse World" map, one of the most popular maps in the game. The map hosts 50,000+ locations and prioritizes having locations from a diverse array of countries. 

**Purpose**

This program retrieves the exact coordinates of the location within second(s). The program returns a google map link which can be used to pinpoint the exact location, allowing the user to earn a perfect score. The program does not access the website in anyway, it strictly used the image of the location provided. 

**User Set Up**

Display Requirements:

1. Display should be a 16:9 aspect ratio. 
2. If you have multiple displays, the geoguessr window should be in your primary display. 

Setting up Geoguessr:

1. Purchase GeoGuessr Pro or sign up for a free trial. The free version with 20 minutes of play per day will not work with this program. 
2. Open up a game of 'A Diverse World'. Link: https://www.geoguessr.com/maps/59a1514f17631e74145b6f47/play
3. To select the 'No Moving, Panning, or Zooming" mode, uncheck 'Use Default Settings' and check 'No move, no pan, no zoom'
4. After you start the game, toggle on fullscreen. Settings are in the bottom left corner. 

Setting up the Location Database: 

The program uses a database of location images from the diverse world map. 

1. Download here (~250mb): https://drive.google.com/file/d/1NEH0feufXZj_C3yuK2zeZvNZmoubpyVD/view?usp=sharing. 
2. Extract and copy the file path to the directory. You will be prompted to enter the file path each time you run the program. 

**Running the Program**

1. Ensure items from user set-up section are followed correctly. If not, the program will continually return "No match found". 
2. Enter in the path to the location database when prompted. 
3. When ready press 'y' to search for the location. 
4. If a match is found, the program will print the google map link as well as copy it to your clipboard. 
5. Use the google map link in reference with the game map to pinpoint the exact location. 
6. When ready, navigate to the next location and repeat steps 3-5. Remember to stay in full screen mode. 
7. When done playing, hit 'q' to quit. 
Note: If you have multiple displays, entering the google map link in a different window will likely be easier as it prevents the constant toggling back and forth between full screen and regular. 

**Methodology**

The program works by comparing an image of the game location with the 50,000 images in the location database. Each database image has locational information such as the latitude, longitude, and directional heading. The database was created through web-scraping the game using Selenium. If the game image can be matched with an image in the location database, than the coordinates can be retrieved and a google maps link can be produced. 

The program uses a content based image retrieval (CBIR) algorithm to return the matching image. Each database image is compared with the game image and scored. If the score is under a certain threshold, the program stops and the image is returned. However, comparing images is not fast, only a couple hundred comparisons can be made per second. Linearly searching through the database of 50,000 images could take a few minutes. 

To solve this, the program estimates the directional heading from the game-provided compass. Directional heading is the angle, for example 0 would be due north and 180 would be due south. The estimate is accurate with .5 degrees on average, up to a max of 2 degrees. After estimating the heading, the program sorts the location images by the proximity to the estimate. This means the program only has to compare a couple hundred images instead of tens of thousands. This reduces the search time from a few minutes down to a couple seconds. 

To estimate the heading from the image of the compass, the program uses template matching. The program rotates a template of the compass incrementally and compares it against the image of the compass in the game. The comparison with the lowest score is the best match and therefore the estimate for the heading. As opposed to a threshold score, the program's goal is to find the minimum score over the range of angles. Like the CBIR algorithm, this is a slow process and linearly working through each angle is not optimal. To reduce the number of template matches, the program implements a ternary search algorithm. 

The template matching scores can be thought of as a unimodal, continuous function. The goal of the algorithm is to estimate the minimum of the function while minimizing the number of calls. The program first finds the lowest score from 0, 90, 180 and 270. The new search range is then cut in half surrounding the best match. For example if the best match, is 90 the new range would be 0 to 180. The function then compares the 1/4, 1/2, and 3/4 markers (in this example, 45, 90, and 135). The new search range is once again cut in half surrounding the best match. On each iteration, the new search range is made to be either the bottom half, middle half, or upper half of the prior search range. Each halving of the function compares 3 values but only calls the template matching function 1-2 times. The middle value of each comparison was always calculated on the previous iteration and doesn't need to be recalculated. Furthermore, the 3/4 value doesnt need to be calcualted if the 1/4 value is less than the mid value. 

A small number of compasses don't produce unimodal functions until within +\- 20 degrees. For example, if the compass is at 0, 180 might have a lower score than 90 even though 90 is closer. For this reason the program first iterates through angles in increments of 20 (instead of 90) to find the best match before proceeding witht the ternary search algorithm. The end result is that it takes 25-30 function calls to estimate the angle within .5 degrees as opposed to the 720 it would take searching linearly. This means it takes under a tenth of a second as opposed to 2+ seconds. 
