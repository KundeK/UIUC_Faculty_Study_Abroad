# Project Summary

Faculty Abroad Connect is a Flask web application that enables UIUC faculty to create a variety of Study and Research Abroad opportunities worldwide. The UIUC faculty, composed of talented scholars and professionals, can use this web application to connect with different institutions, universities, and students from abroad. With web pages that allow faculty to survey and create opportunities abroad, they can explore their professions and help advance the scientific condition of the world through their passions.

## Features

### Web Application Functionality

- **Program Showcase:** Web pages showcasing different programs abroad with details such as city, department, housing, and term.
- **Application Submission:** Allows faculty and foreign students to apply for and create desired programs.
- **Slideshow Feature:** Displays students and programs from around the world for faculty to consider.
- **Recommendation Algorithm:** Suggests opportunities abroad based on program preferences.
- **Web Forum:** Connects external institutions or students from abroad with UIUC faculty members looking for opportunities, enhancing connectivity.

### Database and Hosting

- **MySQL Database:** Hosts information about all programs, including city, department, housing, and term details.
- **CRUD Features:** The application supports various CRUD (Create, Read, Update, Delete) operations for managing program data.
- **GCP Hosting:** The MySQL database is hosted on Google Cloud Platform (GCP) to ensure scalability, reliability, and security.

## Implementation Details

### Web Pages

1. **Setup:**
   - Developed using Flask, HTML, CSS, and JavaScript.
   - Interfaces designed to be user-friendly and intuitive.

2. **Program Display:**
   - Lists various programs abroad with relevant details.
   - Includes search and filter functionality to easily find desired programs.

3. **Application Submission:**
   - Allows faculty and students to submit applications for programs.
   - Forms are validated and processed server-side using Flask.

### Slideshow and Recommendation Algorithm

1. **Slideshow:**
   - Features images and descriptions of students and programs worldwide.
   - Provides inspiration and ideas for faculty to create new opportunities.

2. **Recommendation Algorithm:**
   - Analyzes program preferences.
   - Suggests relevant opportunities to faculty based on their interests and past program engagements.

### Web Forum

1. **Forum Features:**
   - Enables external institutions or students to reach out to UIUC faculty.
   - Facilitates discussions and expressions of interest in collaboration.

### Database Management

1. **MySQL Database:**
   - Stores program information including city, department, housing, and term.
   - Supports CRUD operations for managing data efficiently.

2. **GCP Hosting:**
   - Ensures the database is scalable, reliable, and secure.
   - Provides robust infrastructure for handling large amounts of data and concurrent users.

