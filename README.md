# JetBrains-Academy--Password-Hacker

__Project overview__: In this project, I play a hacker, who connects to a secret server and tries to crack the password in the quickest way possible.

I chose this project because I wanted to learn both a series of modules like _socket_ (or how to connect to a server, send and get information from it) and _itertools_ (or how to create an efficient iterator) and how to use generators in practice.

The project initially is separated by 5 stages:

1. For starters, let’s pretend the admin's website isn't protected at all. Learn how to connect to the server and receive data from it to access private information.
2. OK, the admin has pumped up the server, and it is now password-protected. But the password is probably short. Let's hack it by applying brute force.
3. The admin has picked up on our attempts to access the server, so now it is protected with a more complex password. Maybe the password is long but not unique? Let's hack it using a dictionary of the most common passwords!
4. The admin is really taking the case seriously. Now it is necessary to specify a valid login and password, and the password cannot be cracked by brute force. And yet, there is a vulnerability in the system that you can exploit to identify the admin's login and password.
5. The admin has reacted quickly and made a patch that removes the vulnerability. It's time to look for another one.

_Source_: JetBrains Academy.

The current code matches the 4th stage of the project. To explain why, I have to tell about the difference between the last two stages.

In the stage 4 I have first to find the correct login from the list of the most popular login names by sending each of them to the server until I get the response “Wrong password!”. If I send incorrect login name, I get response “Wrong login!”. Next, I have to hack the password. It is now randomly generated from several characters. However, the message “Exception happened during login” pops up when the symbols of the password match the beginning of the correct one. So, I have to loop through all the symbols until I get the exception message for each position. I do it until I finally receive the message: “Connection success!”

In the stage 5 the exception message disappears, so I no longer know if I added the right symbol to the password. However, since catching the exception takes the computer a long time, there should be a delay in the server response when this exception takes place. So, the solution is to measure time and figure out which iteration takes longer and assume that it is the correct beginning of the password. For this purpose, _time_ module is suggested to use, and namely function _perf_counter()_. 

In my opinion, this final stage is way too artificial and was given only to introduce some functions of the _time_ module like _sleep()_, _perf_counter()_, etc. So, I decided to show off my solution for the stage 4 only.

I am grateful to JetBrains Academy Team for their hard work on making such learning projects and the opportunity to learn. 
