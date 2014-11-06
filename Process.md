
Summary of Planning Meeting (Iteration 1): 
* Opted to use Atlassian's JIRA ticketing system instead of Github's issue tracker. Taras set up a project and an Agile tracking board for the team to use.
* turned the user stories we planned to get done this phase into tech stories
* focus on finding useful packages and libraries to minimize our work, learn to use Django + Angular
* scheduled group meeting for Joseph to give us a crash course in the above
* Joseph set up a template project for us to use as a starting ground
* Tried our hand at estimating story points
* Decided not to do daily scrums so long as we kept in touch via Slack and after classes. meeting every 4 days should be enough to keep things on track


Summary of Sprint Retrospective (Iteration 1):
* Team is feeling lost, lots to learn about Django and Angular
* Application backbone is online, but handful of tickets pushed into next sprint
* Everyone is busy with other coursework
* Still hoping to complete target features, with some minor revisions
* estimating is hard, blew some estimates

Summary of Planning Meeting (Iteration 2): 
* After tasking, problem with dependancies immediately became clear, heavy bottlenecking from blocking tickets in event API creation without the option of multiple people working on same code
* Brought in tickets for webscraping and ROSI integration to make sure everyone has something to do
* Not too worried about meeting every goal of our plan after discussion with Anson about possibly cutting scope back now that we are a 5 person team


Summary of Sprint Retrospective (Iteration 2): 
* JIRA should be kept more up to date with what people are working on, though this wasn't much of a problem as we kept to our own branches and communicated on Slack
* team is getting more confident with Djangular developement
* application is in a demoable state
* ran through topics to cover in presentation

## A summary of our "daily" scrum meetings
#### Oct 17th 5:00
**Joseph** - 
Just added the initial template to the repository. We will plan to meet to go though the code in the next few days. Possibly tomorrow.

**Taras** - 
Been looking into google authentication and how we might do that with Django. Found a potentially useful app called `Django Social Auth`. Will continue investigation.

**Michelle** - 
Looking at the course tables as well as beautiful soup example from Joseph, will continue looking into the structure of the table and how I might parse it.

**Lyon** - 
Reading some Django documentation on models so that I can pickup the tickets on the initial models. I'll sync up with Joseph when I have some code to show him.

**Allen** - 
Given anything I'd like to start working on is blocked, I'll begin looking into phantom JS and using it to get courses given ROSI credentials. I'll sync up with Joseph when I have some code to show him.

#### Oct 22nd 7:00
**Joseph** - 
Taras handed authentication off to me as he's been swamped with other work and I feel like it might block the team. I finished it early this morning/last night. I've also updated the settings to work with our new website http://abarticulus.me which I've taken the liberty of creating and deploying out current application to. Currently displays your second calendar on login, using spaghetti code just to show how it was done.

**Taras** - 
Been looking at your angular code in the authentication section as well as in the app to prepare for adding the initial calendar angular app.

**Michelle** - 
I have some code but there are some issues with it parsing the table. I'll push the code to a branch tonight/tomorrow and Joseph said he'd give me a hand and take a look at it and give it an early code review. I'll work with him to get this closer to being done.

**Lyon** - 
I think I'm ready to start on the models. We had a meeting earlier today about how we want to structure those models now that we've began coding and have a better understanding of the requirements and how to use the Google API.

**Allen** - 
Phantom JS is not very easy but I think I'm starting to understand it. Will keep you guys posted.

#### Oct 26th 5:30
**Joseph** - 
Helping you guys with code reviews as well as helping pick up the initial angular calendat app from Taras. I got a bootstrapped angular application up and running as well as the initital API classes we'll be using to show you guys an approximate structure and idea of how to build them.

**Taras** - 
I began work on the angular application but got really busy with some other work. Due to blocking the frontend work, I handed it off to Joseph to finish up for me. We went through the code I'd written and he revamped it a bit to get it up and running.

**Michelle** - 
Working on the parser stii. Joseph is assisting me and giving me suggestions and code reviews. Next I'm looking into turning this sctipt into a Django Management Command so that I can take what I have and turn into something Django will use to add the information abotu lectures to the database.

**Lyon** - 
Added initial models with the help of Joseph code reviewing as I went and we shipped them already. Going to start looking into some AngularJS tutorials as well as Joseph's example code so that I can start working on the `Create Event` frontend.

**Allen** - 
Started working on the ROSI stuff, xpath selection seemed difficult but apparently I can use CSS selectors so that should make this much easier. Wish I knew that...I'll keep chugging along and keep you guys updated.

#### Nov 1st 2:30
**Joseph** - 
I've done a lot of coding so I've stepped back to answer questions and do code reviews recently. Feel free to ping me if you need help writing things and I'll keep in touch with everyone.

**Taras** - 
Pumped to work on the backend of events, discussed the architecture with Joseph and I'm ready to start this weekend.

**Michelle** - 
Been making significant progress. I think I'm almost ready to begin writing the manegemnt command. Very excited for that.

**Lyon** - 
Feeling a bit better about Angular, going to starting the event creation this weekend!

**Allen** - 
Chugging along. Going to push some code today/tomorrow and I plan to try to be done with this by the end of the weekend then I can join in to helpout with the frontend.

#### Nov 4th 11:30
**Joseph** - 
Have become pull request gatekeeper, making sure code is up to snuff before getting merged to master

**Taras** - 
I now resent time formats and Google's Calendar API, but we have working Event creation. Some fixes left for tomorrow, but it works. 

**Michelle** - 
Scraped data is full of special cases that need to be handled, but it's looking to be in a state that can be demoed for Thursday!

**Lyon** - 
Waiting for Taras to finish his part to hook the UI up to, but the interface is chugging along. 

**Allen** - 
Some problems with getting the headless browser to use ROSI's UI, not likely to get in a demoable state, but this was a stretch goal anyway. 

## Description of how you used GitHub issue management system
We didn't. We used Jira instead and you can checkout [our board](https://csc301.atlassian.net/secure/RapidBoard.jspa?rapidView=4). ([Sprint Report View](https://csc301.atlassian.net/secure/RapidBoard.jspa?rapidView=4&view=reporting&chart=sprintRetrospective&sprint=2)) Joseph and Taras have used it before and so we decided as a team, based on their reccomendation, to try it for this phase. We'll be creating tickets for what we work on and assigning outselves to them. We'll attach the pull request and use it's sprint functionality to track what we plan to do and what we have done. Taras will be, awesomely, taking the lead and creating tickets after out sprint planning meetings. This will help us keep organized. We'll be using Jira's kanban board, instead of the agile one, because it's simpler for the team member who have yet to use JIRA but we'll be using sprints and simply creating tickets at the beginning of the sprint so that the backlog is composed of our current sprint. Each person is allowed to pick up any ticket as long as it's not assigned to anyone.

## Description of any other major decisions/conventions you may have made/used during the process
The only ones I can think of are:

1) No commiting to someone else's branch unless asked. Commenters should generally avoid actually commiting code when reviewing another person's code unless asked to fix something. This is because it's much more effective to learn by doing and by providing code snippets or suggestions as ultimately that person decides what code will go into their branch (even though as the code reviewer you can block them from merging till you pass it).

2) No scrum master
Seems unnecessary for a project our size. We'd rather delegate small tasks to specific people than have their be a master in charge of them all.  We're also pretty busy so no one really wants the overhead of having to do it either. This will be simple if we keep it that way and if we found it had been a poor decision then we'd have elected one.

3) No official daily scrum, but daily updates in Slack chat.
