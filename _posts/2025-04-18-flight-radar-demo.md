---
title: What do community organisers need? Not another pizza.
tags: [Community, Events, Organising, Article]
layout: post
image: /assets/images/pizza_stack.jpg
---

Install raspbian 64 bit lite

Install docker

sudo apt update
sudo apt install -y docker.io

# Install Docker Compose
sudo apt install -y docker-compose

# Add your user to the docker group to run docker without sudo
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect, or run:
newgrp docker