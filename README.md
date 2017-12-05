# Coding Challenge

Write a simple django-rest-framework app starting from the following database structure (**feel free to modify it as you feel fit in order to solve the requirements in the most efficient way**):

![Database structure](https://user-images.githubusercontent.com/32396267/33604919-5a9d9a08-d9c0-11e7-98cd-7de4a3bf82a6.png "Database structure")

## Requirements:
1. The users should be able to login/register (by default when registering, user has no team).
2. After registration, the user should be able to verify their e-mail address.
> **in a real world scenario, the user would open the link received in the e-mail, and the front-end would take care of verifying their e-mail address with the back-end.**
3. The users should be able to reset their passwords. As a suggestion **- however, you can choose to implement this feature your own way -** you could have two routes:
- /reset/ - which triggers the reset password mechanism
- /password/ - which sets the new password from the user
> **in a real world scenario, the user would go to the front-end app, choose forgot password option, put in their e-mail and then after some steps they would be able to set a new password for their account**

> **please consider data privacy when implementing this feature**
4. The users should be able to create their own teams (if they don’t have a team already).
5. The users should be able to invite people to join the platform (register). Once registered through the invitation, the new users will automatically be assigned to the team of the person who invited them.

## Deliverables:
- Publish the code on GitHub, create a Readme file with:
- API docs
- instructions on how to run the project locally
- deployment instructions
- link to live demo on Heroku
