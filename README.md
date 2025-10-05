# ScribbleBug
## Inspiration
We were inspired by the heyday of html5 games as exhibited by "coolmathgames" and others. Could LLMs bring something new to this space? Simon Wilson, co-creator of the Django web framework, also wrote about LLM's game programming abilities on his [blog](https://simonwillison.net/2025/Jul/29/space-invaders/). We wanted to take this one step further and empower users to create their own customized digital experiences.

## What it does
ScribbleBug is an online space for people to create fun mini-games to play and share with others. It uses an LLM internally to generate an online experience for people to use.

## How we built it
We created a full-stack web application using Django on the back-end and Vue.js for client-side interactivity on the keyword selection page.

## Challenges we ran into
- Using the Google API to generate images
- Database migrations

## Accomplishments that we're proud of
- Getting it to work
- Creating a fun-to-use experience

## What we learned
This was our first project using the Django web framework, so it was completely new to us. We also learned how to integrate `auth0` with Django Social Auth to handle user authentication. We learned how to manage our database with the Django ORM.

## What's next for ScribbleBug
- Game leader boards
- Chat with your game to customize and improve it
- Password-less sign-in
- ScribbleBug digital currency to upgrade your games
