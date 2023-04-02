# **Elevator System README**
This README document outlines the thought process, design decisions, and instructions for setting up and testing the Elevator System API developed using Django and Django REST Framework.

# Thought Process
The Elevator System is a simplified model that emulates an elevator system with the ability to move up and down, open and close doors, start and stop, and assign elevators to requests.

# Design Decisions
## Architecture
The Elevator System is built using Django and Django REST Framework, which provides a robust and scalable framework for building APIs. The application follows the Model-View-Controller (MVC) architecture pattern.

## Repository File Structure
The project is organized into several directories:

**elevator_system/**- This directory contains the settings and configuration files for the Django project.\
**elevator/** - This directory contains the models, serializers, and viewsets for the Elevator API. \
**request/** - This directory contains the models, serializers, and viewsets for the Request API.\
**templates/** - This directory contains the HTML templates used for the frontend of the application (not implemented).

# Database Modelling
The Elevator System uses SQLite Database with two models: **Elevator** and **Request**.

## Elevator Model
The Elevator model represents an elevator in the system and has the following fields:

**id:** The id of the elevator (integer). \
**current_floor:** The current floor of the elevator (integer). \
**status:** The status of the elevator (string, either 'idle' or 'moving').\
**direction:** The direction in which the elevator is moving (string, either 'up', 'down', or 'idle'). \
**top_target_floor:** The top target floor in which the top level floor(integer). \
**ground_target_floor:** The ground target floor in which the bottom level floor(integer) \

## Request Model
The Request model represents a user request for an elevator and has the following fields:

**elevator:** The elevator assigned to the request (foreign key to the Elevator model). \
**floor:** The floor where the request is made (integer). \

## Libraries Used
The following libraries are used in the Elevator System:

**Django:** A high-level Python web framework that enables rapid development of secure and maintainable websites and APIs. /
**Django REST Framework:** A powerful and flexible toolkit for building APIs that includes serializers, viewsets, and authentication support. /

# API Contracts
The Elevator System has the following API contracts:

## Elevator API
**GET /elevators/** \
Returns a list of all elevators in the system.

**GET /elevators/{id}/** \
Returns the details of a specific elevator with the given id.

**POST /elevators/{id}/move_up/** \
Moves the elevator with the given id up one floor.

**POST /elevators/{id}/move_down/** \
Moves the elevator with the given id down one floor.

**POST /elevators/{id}/open_door/** \
Opens the door of the elevator with the given id.

**POST /elevators/{id}/close_door/** \
Closes the door of the elevator with the given id.

**POST /elevators/{id}/stop/** \
Stops the elevator with the given id.

**GET /elevators/{id}/next_destination/** \
Returns the next destination floor for the elevator with the given id.

**POST /elevators/** \
Creates a new elevator in the system.

**POST /elevators/{id}/make_maintenance/** \
Mark the elevator to maintenance

## Request API
**GET /requests/** \
Returns a list of all requests in the system.

**GET /requests/{id}/** \
Returns the details of a specific request with the given id.

**POST /requests/** \
Creates a new request in the system.

# Test
To test the application, you can follow these steps:

1. Activate the virtual environment: source **env/scripts/activate**
2. Verify that the responses are correct and the application is functioning as expected.
# Conclusion
The Elevator System API developed using Django and Django REST Framework provides a scalable and efficient solution for managing elevator systems. By following the design decisions outlined in this README, you can easily deploy and test the application to ensure its smooth operation in production.