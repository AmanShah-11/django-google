<h1>Automatic Event Scheduler</h1>

<p>I built this application to help users schedule events when they have a general idea of what they want to do, but don't have a specific location in mind!  </p>

<p>The application takes in information from user input and returns the location of the event and creates an event for it with the invited user in Google Calendar (performed in Django)</p>

<p>These events are then displayed in the React frontend so that users can easily see all of their events and whether they have been completed or not (based on the date or the event). </p>


<p> Users can register for the app through a simple user Django form that takes in basic information.</p>

<p> The React App offers basic CRUD functionality, however the implementation with the Google API is limited to the Django form to allow the user several ways to schedule events with others. </p>

<p>The Google APIs that I used include:</p>
<ul>
    <li>Google Geocoding API</li>
    <li>Google Maps API</li>
    <li>Google Roads API (Future implementation of this app will allow users to get directions to the specified location). </li>
    <li>Google Calendar API</li>
</ul>

<p>
    The things used to build this application include:
    <ul>
        <li>Django</li>
        <li>Django Rest Framework</li>
        <li>Python</li>
        <li>React</li>
        <li>HTML</li>
        <li>CSS</li>
        <li>Javascript</li>
    </ul>
<p>
<p>
Note: You will need to create your own Google API key to successfully run the API calls, and have that Google API key text in the first line of your 
"secrets.txt" file
 </p>

 <p>
 Note: You will need to verify access to your google calendar through an OAuth verification, this happens automatically when the script is ran on a new google account through Quikstart.
 </p>
