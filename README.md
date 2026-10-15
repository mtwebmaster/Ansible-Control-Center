# Ansible Control Center (ACC)
### A Simple Guide to Managing Computers

**Project Overview | Beginner-Friendly Edition**

**Created by:** Jeff Swenson  
**Developed with assistance from:** OpenAI GPT-6  
**Project Status:** Experimental Development  
**License:** MIT

---

## Welcome to Ansible Control Center

### What if one person could take care of an entire team of computers?

Imagine you have five helpful robots.

Each robot has an important job. Some help organize the team, while others do the hard work.

But how do you make sure they're all working properly?

How do you know when one needs help?

How do you tell them what to do without visiting every robot individually?

**That's where Ansible Control Center comes in.**

Ansible Control Center, or **ACC**, is a computer management system that helps one person watch over, organize, and manage many computers from one central location.

Think of it as a control room for your computer team.

---

## 1. Meet Your Computer Team

ACC can help manage groups of computers that work together.

In our example, the team has five computers with two different responsibilities.

### The Leader Computers

**Three computers help manage the team.**

Imagine three team leaders working together to keep everyone organized.

They help make important decisions and keep the computer team operating.

These computers are called *control-plane nodes*, or *masters*.

If one leader has trouble, the others may still be able to help keep things running.

### The Worker Computers

**Two computers help do the work.**

The workers perform jobs, run programs, and handle tasks that need to get done.

They are called *worker nodes*.

### How the Team Works

| Computer Role | Number | Responsibility |
|---|---:|---|
| Leaders (Masters) | 3 | Help coordinate and manage the team |
| Workers | 2 | Perform tasks and run programs |
| **Total** | **5** | **Work together as one team** |

When these computers work together using MicroK8s, we call them a **computer cluster**.

A cluster is simply a group of computers cooperating to accomplish a bigger job.

---

## 2. Your Computer Control Room

Imagine sitting inside a spaceship.

In front of you is a control panel that shows what's happening throughout the entire ship.

Instead of walking to every room, you can see important information from your seat.

**ACC works in a similar way.**

It provides a central place where a computer administrator can check the computers and choose operations to perform.

The control room can display information such as:

- Which computers are responding
- How busy the computers are
- Whether important services appear healthy
- Which computers may need attention
- Whether recent backup information is available

ACC's control panel runs inside a computer terminal, using menus and text.

This is called a **Terminal User Interface (TUI)**.

It allows an administrator to manage computer systems without needing a traditional graphical desktop.

---

## 3. Sending Instructions to Your Computers

Imagine you have five robots and want each one to tidy its workspace.

You could tell them individually.

But wouldn't it be easier to give one set of instructions and have a helper deliver it?

That's what **Ansible** does.

Ansible is software that helps administrators send instructions to computers.

ACC helps organize and launch those instructions from one place.

For example, an administrator might use ACC and Ansible to check whether computers are available, inspect system information, or perform approved maintenance operations.

**The goal is simple: make computer management more organized and reduce repetitive work.**

---

## 4. Keeping an Eye on Computer Health

Computers can have problems, just like other machines.

They can become too busy, run low on storage, stop responding, or experience software failures.

Imagine having a friendly helper who regularly checks whether your robots are doing okay.

ACC includes monitoring tools designed to do something similar.

### What Does ACC Monitor?

ACC can collect information about computer activity, including processor usage, memory, disk space, and system availability.

It can also track certain alerts and changes over time.

The collected information is stored in a small local database called **SQLite**.

Think of SQLite as a digital notebook that remembers how the computers have been doing.

This helps administrators recognize problems and investigate when something changes.

---

## 5. Protecting the Important Computers

Not every computer should be allowed to perform every action.

Imagine a worker robot accidentally entering the main control room and pressing a button that shuts down the entire team.

That could cause serious trouble.

ACC includes safety rules designed to help prevent these kinds of mistakes.

### Important Safety Rules

**Rule 1 — Know who belongs on the team.**

ACC checks configured computer identities and roles before allowing certain operations.

**Rule 2 — Protect the leaders.**

Ordinary worker maintenance should not accidentally change or restart the control-plane computers.

**Rule 3 — Don't trust unknown computers.**

A computer that isn't recognized should not automatically receive permission to perform maintenance operations.

**Rule 4 — Ask before making important changes.**

Certain operations require the administrator to confirm the action before continuing.

These protections help make computer management safer.

However, ACC is still under development, and its security controls require additional testing.

---

## 6. Giving Computers a Break

Even hardworking robots sometimes need maintenance.

Computers may need software updates or restarts to keep operating properly.

But what happens when a worker computer is already busy?

Imagine a robot carrying an important package. You wouldn't want to turn it off before it finished its job.

ACC includes a maintenance workflow designed to help administrators prepare worker computers for maintenance.

The process can involve:

1. Preventing a worker from receiving new jobs.
2. Moving certain existing work away when possible.
3. Performing approved maintenance.
4. Restarting the worker if necessary.
5. Checking whether the worker is ready to return.
6. Allowing the worker to receive jobs again.

In Kubernetes, parts of this process are called **cordoning** and **draining**.

Some workloads cannot move automatically, so these steps still require careful supervision.

The leader computers require separate, especially careful procedures to avoid disrupting the whole cluster.

---

## 7. Creating Safety Copies of Important Information

Imagine building a wonderful LEGO castle.

You spend hours putting every piece in the right place.

Now imagine the castle accidentally gets knocked over.

Wouldn't it be helpful to have a way to rebuild it?

A computer backup serves a similar purpose.

ACC includes tools designed to create protected copies of important MicroK8s datastore information.

### How the Backup System Works

The backup system is designed to:

- Connect securely to an approved computer.
- Retrieve important backup information.
- Save the backup in a dedicated storage location.
- Check the saved archive for certain integrity problems.
- Record information about the backup result.

These steps help administrators protect important data.

**Important:** A backup is only truly useful when the information can be successfully restored. ACC's full restoration procedure still needs to be validated.

---

## 8. Keeping the Computer Team Secure

Imagine your computer team works inside a clubhouse.

You wouldn't want strangers walking through the door and changing everything.

You would want locks, keys, and a way to recognize authorized visitors.

Computer security works in a similar way.

ACC includes tools that use secure connections, restricted accounts, certificates, and temporary access tokens.

These help computers recognize trusted connections and limit access to important operations.

Private keys, passwords, certificates containing sensitive information, and other credentials must be protected and should never be placed in a public software repository.

The goal is to keep the computer control room accessible only to the people and systems that should use it.

---

## 9. What's Inside Ansible Control Center?

Think of ACC as a toolbox with different compartments.

Every compartment holds tools for a particular job.

| Component | What It Does |
|---|---|
| `src/` | Contains ACC's main interface and core software |
| `ansible/` | Holds instructions used to manage computers |
| `monitoring/` | Contains tools that check computer health |
| `backup/` | Holds tools for creating and verifying backups |
| `kubernetes/` | Contains cluster health and security utilities |
| `config/` | Stores example configuration and templates |
| `docs/` | Provides instructions and technical explanations |
| `systemd/` | Contains service definitions for automated background tasks |

All these parts work together to support ACC's larger purpose.

---

## 10. Is Ansible Control Center Ready for Everyone?

ACC is a real software project built from an operational Linux and MicroK8s management environment.

Many of its components have already been developed, and selected features have passed focused tests.

However, the portable release still requires additional work.

### Completed Foundations

- Core terminal management interfaces
- Ansible management functionality
- Computer role authorization modules
- MicroK8s health inspection utilities
- Monitoring and alert collection components
- Backup scripts and integrity checks
- Configuration examples
- Source code published on GitHub

### Still Being Developed

- A complete, easy-to-use installer
- Broader security and functionality tests
- Verified backup restoration instructions
- Improved deployment documentation
- Reproducible demonstrations
- Additional automation and reliability improvements

**Current status: Experimental.**

This version is intended for technical review, learning, and development. It should not replace an important working installation without proper testing.

---

## 11. Making ACC Better in the Future

The long-term goal is to make ACC a dependable and easy-to-understand control center for managing Linux computers and MicroK8s clusters.

Future improvements will focus on making setup easier, strengthening safeguards, improving tests, and documenting reliable maintenance and recovery procedures.

The vision is to give administrators one organized place to understand their systems and carry out approved operations with confidence.

---

## 12. Sharing the Project with Others

ACC's source code is available through GitHub.

GitHub allows developers to share software projects, review changes, suggest improvements, and work together.

ACC is released under the **MIT License**, allowing others to use, modify, and share the software under its license terms.

**Project Repository:**  
[Ansible Control Center — GitHub](https://github.com/mtwebmaster/Ansible-Control-Center)

Community feedback, testing, documentation improvements, and contributions can help make the project better.

---

## The Big Picture

Ansible Control Center helps answer four important questions:

**1. Are my computers working properly?**

ACC provides monitoring information and health checks.

**2. Can I manage them from one place?**

ACC organizes Ansible operations through a central terminal interface.

**3. Can I protect important systems from mistakes?**

ACC includes role-based safety controls, confirmation prompts, and security utilities.

**4. Can I protect important information?**

ACC includes backup and verification tools designed to support data protection and recovery planning.

### In Simple Terms

**Ansible Control Center is like a smart clubhouse manager for a team of computers. It helps the team stay organized, watches for problems, assists with maintenance, and provides tools designed to protect important information.**

---

## Project Information

**Project:** Ansible Control Center (ACC)  
**Creator:** Jeff Swenson  
**Development Assistance:** OpenAI GPT-6  
**License:** MIT  
**Platform:** Linux  
**Current Release Status:** Experimental  
**Source Code:** https://github.com/mtwebmaster/Ansible-Control-Center

*This document is a simplified educational introduction. For technical instructions, system requirements, configuration details, and safety limitations, refer to the project's primary README and technical documentation.*
