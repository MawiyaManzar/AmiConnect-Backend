-- AmiConnect PostgreSQL Schema

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female')),
    department VARCHAR(20) CHECK (department IN ('BTech', 'BCA', 'MCA','BBA')),
    year INTEGER CHECK (year >= 1 AND year <= 6),
    connection_type VARCHAR(30) CHECK (connection_type IN ('Study Partner', 'Project Collaboration', 'General', 'Friendship')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS interests (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS learning_goals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Association tables
CREATE TABLE IF NOT EXISTS user_interests (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    interest_id INTEGER REFERENCES interests(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, interest_id)
);

CREATE TABLE IF NOT EXISTS user_skills (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, skill_id)
);

CREATE TABLE IF NOT EXISTS user_learning_goals (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    learning_goal_id INTEGER REFERENCES learning_goals(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, learning_goal_id)
);
