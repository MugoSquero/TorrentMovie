# TorrentMovie

## Simple explanation
This Python script searches for and downloads movie torrent files from the internet.

## What it does?

This script is a program written in the Python programming language that allows a person to search for and download a movie file from the internet. The script does this by sending requests to a website called YTS.mx and receiving information back from the website. The script then processes this information and presents the user with a list of movies to choose from.

The script begins by importing the necessary libraries and disabling warnings for the requests library. It then defines a few functions to handle the scraping and downloading of the torrent file.

The script prompts the user to input either the IMDb title (in the format "tt[0-9]*") or the name of a movie. If the user inputs an IMDb title, it sends a request to YTS.mx using the requests library and presents the user with a list of 5 movies matching the search query. If the user inputs a movie name, it does the same but also checks if the movie is available on YTS.mx. If it is, it just downloads the torrent files with 720p.BlueRay and 1080p.BlueRay (if there is no option for BlueRay, it prompts user to download the WEBrip). If movie is not available on YTS.mx, it prompts the user to select an alternative search and, if the user agrees, performs an alternative search using a different website (snowfl).

Once the user has selected a movie, the script prompts the user to select a torrent for the movie from a list of available torrents. It then attempts to download the selected torrent using one of the functions defined earlier. If the download is successful, it prints a message indicating that the download is complete and exits the program. If the download fails, it prints an error message and exits the program.

It saves torrent files to the location D:\Movies. If you want to keep it just create a folder in your D drive. Or if you want to change it, just edit the script to your willing.

## Installation

Just install requests library and you are done.
