import os
import socket
import streamlit as st
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
     page_title="Hello Streamlit App",
     page_icon="🧊",
     layout="centered",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )

components.html(
'''
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Geolocation example: Checking for geolocation support</title>
        <meta charset="utf-8"; content="text/javascript">
    </head>
    <body>
        <h1>Hello, This site is to check for geolocation support</h1>
        <p>
            <input type="button" onclick="show_islocationenabled();" value="Is Geolocation supported?" />
        </p>
        <div></div>
        <div></div>
        <div></div>
        <script>
            document.write('Javascript for geolocation check<br><br>')
            var useragent = window.navigator.userAgent;
            document.write(useragent+'<br><br>');

            function show_islocationenabled() {
                console.log(window.navigator.geolocation)
                console.log(navigator)
                console.log(navigator.geolocation)
                var str = "No, geolocation is not supported.";
                if (window.navigator.geolocation) {
                    str = "Yes, geolocation is supported.";
                    navigator.geolocation.getCurrentPosition(successFunc,notsuccessFunc);
                }
                document.getElementsByTagName('div')[0].innerHTML = str+'<br><br>';
            }
            
            // console.log(window.navigator)
            // document.write(navigator.geolocation,'<br>')
            // document.write(navigator)

            function successFunc( position )
            {
                
                str = 'latitude:' + String(position.coords.latitude) + '&deg;<br><br>';
                // document.getElementsByTagName('div')[1].textContent = str;
                // document.getElementsByTagName('div')[1].innerText = str;
                document.getElementsByTagName('div')[1].innerHTML = str;
                
                str = 'longitude:'+position.coords.longitude+'&deg;<br><br>';
                document.getElementsByTagName('div')[2].innerHTML = str;

                // document.write('Positon<br>')
                // document.write('longitude:',position.coords.longitude,'&deg;<br>');
                // document.write('latitude:',position.coords.latitude,'&deg;<br>');
            }
            function notsuccessFunc()
            {
                document.getElementsByTagName('div')[1].innerHTML = 'Could not get GeoPositions.<br><br>';
            }
        </script>

    </body>
    </html>
''', height=600
)

st.write('Hello Streamlit again!!!')
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

st.write(hostname,ip)

st.write(dict(os.environ))

st.write('hello<br>hello<br>')
