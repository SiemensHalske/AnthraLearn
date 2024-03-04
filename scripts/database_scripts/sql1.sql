-- Schritt 1: Datenbank erstellen (Führe diesen Befehl direkt in deinem SQL-Client oder der Konsole aus)
-- CREATE DATABASE anthralearn;

-- Schritt 2: Mit der erstellten Datenbank verbinden (Diesen Schritt in deinem SQL-Client oder Tool durchführen)

-- Schritt 3: Schema erstellen, falls noch nicht vorhanden (Diesen Befehl in der Datenbank `anthralearn` ausführen)
CREATE SCHEMA IF NOT EXISTS public;

-- Nun folgen die CREATE TABLE Befehle innerhalb des Schemas `public`:

CREATE TABLE public.Users (
    UserID SERIAL PRIMARY KEY,
    Username VARCHAR(255) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    ProfilePicture VARCHAR(255),
    RegistrationDate DATE NOT NULL
);

CREATE TABLE public.Roles (
    RoleID SERIAL PRIMARY KEY,
    RoleName VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE public.UserRoles (
    UserID INT REFERENCES public.Users(UserID),
    RoleID INT REFERENCES public.Roles(RoleID),
    PRIMARY KEY (UserID, RoleID)
);

CREATE TABLE public.Courses (
    CourseID SERIAL PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    CreatorID INT REFERENCES public.Users(UserID),
    PublicationDate DATE NOT NULL,
    Status VARCHAR(50) NOT NULL
);

CREATE TABLE public.Modules (
    ModuleID SERIAL PRIMARY KEY,
    CourseID INT REFERENCES public.Courses(CourseID),
    Title VARCHAR(255) NOT NULL,
    Description TEXT,
    Sequence INT NOT NULL
);

CREATE TABLE public.Lessons (
    LessonID SERIAL PRIMARY KEY,
    ModuleID INT REFERENCES public.Modules(ModuleID),
    Title VARCHAR(255) NOT NULL,
    ContentType VARCHAR(50) NOT NULL,
    Content TEXT NOT NULL,
    Sequence INT NOT NULL
);

CREATE TABLE public.UserProgress (
    ProgressID SERIAL PRIMARY KEY,
    UserID INT REFERENCES public.Users(UserID),
    CourseID INT REFERENCES public.Courses(CourseID),
    Status VARCHAR(50) NOT NULL,
    CompletionDate DATE
);

CREATE TABLE public.Assignments (
    AssignmentID SERIAL PRIMARY KEY,
    LessonID INT REFERENCES public.Lessons(LessonID),
    Title VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    DueDate DATE NOT NULL
);

CREATE TABLE public.Submissions (
    SubmissionID SERIAL PRIMARY KEY,
    AssignmentID INT REFERENCES public.Assignments(AssignmentID),
    UserID INT REFERENCES public.Users(UserID),
    SubmissionDate DATE NOT NULL,
    File VARCHAR(255),
    Grade INT,
    Feedback TEXT
);

CREATE TABLE public.DiscussionForums (
    PostID SERIAL PRIMARY KEY,
    CourseID INT REFERENCES public.Courses(CourseID),
    UserID INT REFERENCES public.Users(UserID),
    Title VARCHAR(255) NOT NULL,
    Content TEXT NOT NULL,
    CreationDate DATE NOT NULL
);

CREATE TABLE public.AdminUsers (
    AdminUserID INT REFERENCES public.Users(UserID),
    AdminRole VARCHAR(255) NOT NULL
);

CREATE TABLE public.CourseAccessRights (
    AccessID SERIAL PRIMARY KEY,
    CourseID INT REFERENCES public.Courses(CourseID),
    UserID INT REFERENCES public.Users(UserID)
);

CREATE TABLE public.AuditLogs (
    LogID SERIAL PRIMARY KEY,
    ActivityType VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    UserID INT REFERENCES public.Users(UserID),
    DateTime TIMESTAMP NOT NULL
);

CREATE TABLE public.Feedbacks (
    FeedbackID SERIAL PRIMARY KEY,
    CourseID INT REFERENCES public.Courses(CourseID),
    UserID INT REFERENCES public.Users(UserID),
    Rating INT NOT NULL,
    Comment TEXT,
    DateTime TIMESTAMP NOT NULL
);
