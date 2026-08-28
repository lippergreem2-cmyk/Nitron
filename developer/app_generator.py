import os

PROJECTS = os.path.expanduser("~/Nitron/generated_projects")

os.makedirs(PROJECTS, exist_ok=True)


def create_app(name):

    folder = os.path.join(
        PROJECTS,
        name.replace(" ", "_").lower()
    )

    os.makedirs(folder, exist_ok=True)

    manifest = """<?xml version="1.0" encoding="utf-8"?>
<manifest package="com.nitron.app">

    <application
        android:label="Nitron App">

        <activity
            android:name=".MainActivity">

            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>

                <category
                    android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>

        </activity>

    </application>

</manifest>
"""

    java = """public class MainActivity {

    public static void main(String[] args){

        System.out.println("Hello from Nitron!");

    }

}
"""

    with open(os.path.join(folder, "AndroidManifest.xml"), "w") as f:
        f.write(manifest)

    with open(os.path.join(folder, "MainActivity.java"), "w") as f:
        f.write(java)

    return f"Android app '{name}' created successfully in {folder}."


def calculator():
    return create_app("Calculator")


def weather():
    return create_app("Weather App")


def notes():
    return create_app("Notes App")


def media_player():
    return create_app("Media Player")
