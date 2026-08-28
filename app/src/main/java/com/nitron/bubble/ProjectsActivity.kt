package com.nitron.bubble

import android.app.AlertDialog
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView

class ProjectsActivity : AppCompatActivity() {

    private lateinit var projectList: RecyclerView
    private lateinit var emptyProjects: TextView

    private val projects =
        mutableListOf<String>()

    private lateinit var projectAdapter: ProjectAdapter

    companion object {
        private const val PREFS_NAME = "nitron_projects"
        private const val PROJECTS_KEY = "projects"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.projects)

        projectList =
            findViewById(R.id.projectList)

        emptyProjects =
            findViewById(R.id.emptyProjects)

        loadProjects()
        setupList()

        findViewById<Button>(R.id.newProjectButton)
            .setOnClickListener {
                showCreateProjectDialog()
            }
    }

    private fun loadProjects() {

        val prefs =
            getSharedPreferences(
                PREFS_NAME,
                MODE_PRIVATE
            )

        val saved =
            prefs.getStringSet(
                PROJECTS_KEY,
                emptySet()
            ) ?: emptySet()

        projects.clear()

        // Sort projects so the list is predictable.
        projects.addAll(
            saved.sorted()
        )

        updateEmptyState()
    }

    private fun setupList() {

        projectAdapter =
            ProjectAdapter()

        projectList.layoutManager =
            LinearLayoutManager(this)

        projectList.adapter =
            projectAdapter
    }

    private fun showCreateProjectDialog() {

        val input =
            EditText(this)

        input.hint =
            "Project name"

        input.setSingleLine(true)

        val dialog =
            AlertDialog.Builder(this)
                .setTitle("New Project")
                .setView(input)
                .setNegativeButton(
                    "Cancel",
                    null
                )
                .setPositiveButton(
                    "Create",
                    null
                )
                .create()

        dialog.setOnShowListener {

            dialog.getButton(
                AlertDialog.BUTTON_POSITIVE
            ).setOnClickListener {

                val name =
                    input.text
                        .toString()
                        .trim()

                if (name.isEmpty()) {

                    input.error =
                        "Enter a project name"

                    return@setOnClickListener
                }

                if (projects.contains(name)) {

                    input.error =
                        "Project already exists"

                    return@setOnClickListener
                }

                saveProject(name)

                dialog.dismiss()

                // Open the new project immediately.
                openProject(name)
            }
        }

        dialog.show()
    }

    private fun saveProject(name: String) {

        projects.add(name)

        saveProjectList()

        projectAdapter.notifyItemInserted(
            projects.size - 1
        )

        updateEmptyState()
    }

    private fun saveProjectList() {

        getSharedPreferences(
            PREFS_NAME,
            MODE_PRIVATE
        )
            .edit()
            .putStringSet(
                PROJECTS_KEY,
                projects.toSet()
            )
            .apply()
    }

    private fun openProject(name: String) {

        val intent =
            Intent(
                this,
                ProjectChatActivity::class.java
            )

        intent.putExtra(
            "project_name",
            name
        )

        startActivity(intent)
    }

    private fun updateEmptyState() {

        emptyProjects.visibility =
            if (projects.isEmpty()) {
                View.VISIBLE
            } else {
                View.GONE
            }
    }

    private inner class ProjectAdapter :
        RecyclerView.Adapter<ProjectHolder>() {

        override fun onCreateViewHolder(
            parent: ViewGroup,
            viewType: Int
        ): ProjectHolder {

            val view =
                layoutInflater.inflate(
                    R.layout.project_item,
                    parent,
                    false
                )

            return ProjectHolder(view)
        }

        override fun onBindViewHolder(
            holder: ProjectHolder,
            position: Int
        ) {

            val name =
                projects[position]

            holder.name.text =
                name

            holder.itemView.setOnClickListener {
                openProject(name)
            }
        }

        override fun getItemCount(): Int =
            projects.size
    }

    class ProjectHolder(
        view: View
    ) : RecyclerView.ViewHolder(view) {

        val name: TextView =
            view.findViewById(
                R.id.projectName
            )
    }
}
