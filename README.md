# AmiConnect Backend
# AmiConnect
Visit the site-: https://amiconnect.vercel.app/

AmiConnect is a web application designed to foster meaningful connections among Amity University students by matching them based on shared interests, skills, and learning goals. Built for the Amity Centre for Happiness, it aims to enhance social well-being and emotional intelligence through peer collaboration, aligning with the centre's mission to build a resilient, joyful, and compassionate society.

## Features

### Current Features
![image](https://github.com/user-attachments/assets/b99ea8af-a003-4cac-a1e8-d91f31acf04a)
![image](https://github.com/user-attachments/assets/4d35190a-e518-40ba-9720-31acb7cffdc8)
![image](https://github.com/user-attachments/assets/bd715dbf-1af4-498e-8455-39e1c0b0d000)




- **User Registration (Signup):**
  - Students register with their Amity email (%@s.amity.edu), name, gender, department, year, connection type (e.g., Study Partner, Project Collaboration), interests, skills, and learning goals.
  - Secure password hashing using bcrypt.
  - Email validation ensures only Amity students can sign up.
  - Interests, skills, and learning goals are stored in a PostgreSQL database with many-to-many relationships.

- **User Authentication (Login):**
  - Students log in with their email and password.
  - JWT (JSON Web Token) issued upon successful login for secure access to protected endpoints.
  - Tokens expire after 24 hours for security.

- **User Listing (`/users` Endpoint):**
  - Displays a list of registered users, filterable by department and year.
  - Protected by JWT authentication to ensure only logged-in users can access.

- **Database Integration:**
  - Uses PostgreSQL hosted on Supabase for robust data storage.
  - Schema includes tables for users, interests, skills, learning_goals, and their associations (user_interests, user_skills, user_learning_goals).

- **API Endpoints:**
  - `POST /signup`: Register a new user.
  - `POST /login`: Authenticate and receive a JWT.
  - `GET /users`: Retrieve filtered user list (in development).
  - *Planned:* `GET /recommend/<user_id>` for personalized user recommendations.

## Technical Stack

- **Backend:** Flask (Python) for API development.
- **Database:** PostgreSQL on Supabase for data storage.
- **Authentication:** bcrypt for password hashing, pyjwt for JWT tokens.
- **Environment:** Managed via `.env` with `python-dotenv`.
- **Deployment:** Planned for Render (backend) and Supabase (database).

## Challenges Faced as a Newbie

As a beginner in web development and database management, I encountered several challenges during the development of AmiConnect:

1. **Setting Up PostgreSQL with Supabase:**
   - *Issue:* Connecting to the Supabase database was difficult due to unfamiliarity with PostgreSQL and Supabase's configuration.
   - *Details:* Errors like `psql: command not recognized` (due to psql not being installed) and `connection refused` (due to network restrictions or incorrect credentials) were frequent.
   - *Solution:* Installed PostgreSQL client tools, updated the PATH environment variable, and configured Supabase to allow all IPs temporarily. Added `?sslmode=require` to the `DATABASE_URL` to handle SSL requirements.
   - *Learning:* Gained experience with database connection strings, SSL, and Supabase's dashboard for managing tables and SQL queries.

2. **Installing Tools on Windows:**
   - *Issue:* Installing `psql` and Chocolatey was challenging due to PowerShell's execution policy restrictions.
   - *Details:* Encountered `running scripts is disabled` when trying to install Chocolatey, requiring a change to the execution policy.
   - *Solution:* Set the execution policy to `RemoteSigned` using `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, then installed Chocolatey and PostgreSQL client tools.
   - *Learning:* Understood PowerShell security settings and package management with Chocolatey.

3. **Understanding Flask and API Development:**
   - *Issue:* New to Flask, building RESTful APIs (e.g., `/signup`, `/login`) and handling JSON requests was complex.
   - *Details:* Struggled with Blueprint organization, request parsing, and error handling.
   - *Solution:* Followed tutorials, used Flask's documentation, and implemented error handling with `try-except` blocks. Leveraged `auth.py` structure for modularity.
   - *Learning:* Mastered Flask Blueprints, JSON handling, and API testing with `curl`.

4. **Database Schema and Relationships:**
   - *Issue:* Designing and implementing many-to-many relationships (e.g., `user_interests`) was initially confusing.
   - *Details:* Errors like `relation does not exist` occurred when tables weren't created.
   - *Solution:* Applied the schema via Supabase's SQL Editor and verified tables using `psql` and Supabase's Table Editor.
   - *Learning:* Learned SQL table creation, foreign keys, and `ON DELETE CASCADE` for data integrity.

5. **Security Concerns:**
   - *Issue:* Accidentally shared sensitive credentials (`DATABASE_URL`, `SECRET_KEY`) during development.
   - *Details:* Required resetting the Supabase password and generating a new `SECRET_KEY`.
   - *Solution:* Reset credentials, added `.env` to `.gitignore`, and learned to secure sensitive data.
   - *Learning:* Importance of environment variable management and version control practices.

## Future Goals

### Expand to All Streams of Students
- **Objective:** Make AmiConnect inclusive for students across all academic streams at Amity University (e.g., Engineering, Management, Arts, Sciences).
- **Implementation:**
  - Enhanced Department Options: Update the `department` field in the `users` table to include all Amity programs (e.g., BBA, BA, MSc). Remove the current `CHECK` constraint limiting to BTech, BCA, MCA, BBA.
  - Customized Matching: Adjust the recommendation algorithm to account for interdisciplinary interests (e.g., a BTech student interested in Psychology collaborating with a BA Psychology student).
  - Stream-Specific Features: Add filters for stream-specific events, courses, or projects to cater to diverse academic needs.
- **Impact:** Broaden the platform's reach, fostering cross-disciplinary collaboration and inclusivity.

### Add Real-Time Chat Option
- **Objective:** Enable students to communicate directly within AmiConnect to discuss projects, study plans, or shared interests.
- **Implementation:**
  - **Technology:** Integrate WebSocket-based real-time chat using Flask-SocketIO or a third-party service like Supabase Realtime.
  - **Features:**
    - One-on-one chat between matched users.
    - Group chat for project teams or interest-based communities.
    - Message storage in a new `messages` table (`sender_id`, `receiver_id`, `content`, `timestamp`).
    - Notifications for new messages.
  - **Security:** Encrypt messages, authenticate users via JWT, and implement rate limiting to prevent spam.
  - **UI:** Add a chat interface to the frontend (planned for Streamlit or React), with real-time message updates.
- **Challenges:**
  - Learning WebSocket protocols and Flask-SocketIO.
  - Ensuring scalability for real-time messaging.
  - Designing a user-friendly chat UI.
- **Impact:** Enhance user engagement, enabling seamless collaboration and strengthening peer connections.

### Additional Goals
- **Recommendation Algorithm (`/recommend/<user_id>`):**
  - Implement a matching algorithm assigning +30 points for shared interests, +20 for skill-goal matches, +10 for same department, and +5 for same year.
  - Return top 5 matches based on total score.
- **Scalability and Performance:**
  - Use connection pooling (`psycopg2.pool`) for database efficiency.
  - Implement rate limiting with Flask-Limiter to prevent abuse.
- **User Feedback:**
  - Add a feedback form to collect user insights on matches and platform usability.
  - Use feedback to refine the matching algorithm and UI.

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-feature`).
3. Commit changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a pull request.

## License
This project is licensed under the **MIT License**.

## Acknowledgments
- **Amity Centre for Happiness** for project inspiration.
- **Supabase** for hosting the PostgreSQL database.
- **Flask and PostgreSQL communities** for robust tools and documentation.
  


