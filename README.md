
# Demo
https://user-images.githubusercontent.com/77243080/202915035-b649da26-aa31-41fe-8b50-4f9f7410e1ce.mp4

## Inspiration

Ever noticed how the music you are listening to has a mental and physical impact on you? From reducing stress and improving cognitive performance, to inspiring creativity, the way we listen to music has been proven to be crucial to our day-to-day experience. Our aim at Happify.ai is to optimise your mood and focus by helping you choose your songs based on your current mood and focus level, boosting your productivity and mental health.

## What it does

Happify.ai is essentially a smart radio application. It provides you with the best song choices to uplift your mood when you are down or keep you focused when your energy level is low, all of which are decided with our algorithm that is based on facial emotional analysis. The user will give their Spotify credentials when they first use the website before dragging their existing playlists in the 4 categories. The application then runs in the background, analyzing their facial expressions all while the user is performing their task. If the user starts to show signs of fatigue, happify.ai enqueues an energetic song to boost the energy of the user. If the user shows signs of sadness, the next songs they will hear will be uplifting, etc. Songs are picked based on our innovative algorithm that ensures a smooth transition between songs and playlists based on the song characteristics (energy level, danceability, tempo etc.).

The implementation can also be adapted into a hands-free version for drivers whereby it is activated by voice and can be voice interactive with drivers which can even take into account the tone of the drivers on top of their facial expressions when making recommendations. This can potentially keep the drivers entertained and awake ensuring both the enjoyability of the drive as well as the safety of it. This can potentially help solve a pain-point as part of the 123LoadBoard Challenge.

## How we built it

Facial expression analysis is done with different models providing information about the fatigue level and emotions respectively which are considered as part of a more holistic approach. We used DeepFace technology in order to classify emotions and then used a cascade classifier model that monitors The Eye Aspect Ratio (EAR) to classify fatigue. Images are captured from the webcam using OpenCV before being passed into the models.

In order to display the progress of the model and authenticate the user, we used a Flask backend and a Vue.js webapp that shows live statistics as well as song informations.

When initialized, the backend obtains the user authentication from Spotify using Spotipy and OAuth2.0. The user then select playlists for each of the quadrant representing the different emotions by dragging and dropping them.

Once the playlists are sent to the backend, it starts the model which runs in the background, continuously updating sentiment statistics. These are then live-streamed to the front-end using websockets, along with the user's current Spotify song and previously played songs. When a song is about to end, we analyze the user's playlists and propose the next song from the respective playlists based on our algorithm which optimizes the user's mood, then select the best song based on their current mood by analyzing meta-information about the songs.

Stack: Python, Vue.js, Flask, Tailwind CSS

Libraries of Interest: Tensorflow, Dlib, OpenCV, PostCSS, DeepFace, Vue-Draggable, Flask Sockets, Pandas, Spotipy

## Challenges we ran into

One of the major challenges was setting up dependencies. It was very hard for us to get one computer that had everything running on it because of the different machine learning and web development dependencies due to the nature of the open-source models.

Another issue we had was with the Spotify API. We had to be careful when developing because when we used WebSockets and because of the refreshing virtual DOM we could get multiple instances of dead WebSockets going which would increase background API calls.

A recurring theme that came back to bite us was threading in the Flask app. We had multiple components that needed to be running at the same time, including the ML, websocket updaters and Spotify math calculations. Because of this, we had to solve concurrency and locking issues, as well as figuring out how to optimally piece out the components.

Accomplishments that we're proud of

As a team, we believe in the applicability and novelty of our project as it requires little input from the user and works as a background task. We are proud of the fact that this project combines common ML concepts in a basic yet original way displayed by an aesthetically pleasing UI. We also believe that this idea has many usages past a desktop app and could be adapted to many different types of strenuous or uninteresting tasks that need a lot of concentration.

## What we learned

For the web stack components, Flask was new to us as well as HTML draggable components and all the associated events. We also learned a lot about websockets and interacting with them through virtual DOMs.

For the AI, we learned how to use open source ml-models and a lot about the process of pipelining them.

## What's next for Happify.Ai

An extension of this project could be to display the collected data (moods) over time and integrate a voice command/bot system for a hands-free user experience. For truckers specifically, we could also add a feature analyzing the overall tiredness of a driver and suggest activities or breaks.
