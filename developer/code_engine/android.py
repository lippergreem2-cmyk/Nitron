import os


class AndroidGenerator:

    def __init__(self):

        self.output = "GeneratedProjects"
        os.makedirs(
            self.output,
            exist_ok=True
        )


    def create_app(self, name):

        project = os.path.join(
            self.output,
            name
        )


        folders = [
            "app/src/main/java/com/nitron/app",
            "app/src/main/res/layout",
            "app/src/main/res/drawable"
        ]


        for folder in folders:

            os.makedirs(
                os.path.join(project, folder),
                exist_ok=True
            )


        files = {

"settings.gradle":
"""
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

rootProject.name="NitronApp"
""",


"app/src/main/res/layout/activity_main.xml":
"""
<LinearLayout
xmlns:android="http://schemas.android.com/apk/res/android"
android:layout_width="match_parent"
android:layout_height="match_parent"
android:gravity="center">

<TextView
android:layout_width="wrap_content"
android:layout_height="wrap_content"
android:text="Created by Nitron AI"/>

</LinearLayout>
""",


"app/src/main/java/com/nitron/app/MainActivity.kt":
"""
package com.nitron.app

import android.app.Activity
import android.os.Bundle


class MainActivity : Activity(){

override fun onCreate(
savedInstanceState: Bundle?
){

super.onCreate(savedInstanceState)

setContentView(
R.layout.activity_main
)

}

}
"""
        }


        for filename, content in files.items():

            path = os.path.join(
                project,
                filename
            )

            with open(path, "w") as f:
                f.write(content)


        return f"Android app created: {project}"
