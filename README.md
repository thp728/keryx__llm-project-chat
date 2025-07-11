﻿# Keryx

Keryx is a web application designed to help users organize their LLM-based chats by project, ensuring each chat within a project adheres to a set of common, project-specific base instructions.


## Features

- **Project-based Chat Organization:** Group your LLM conversations by project.
- **Customizable Project Instructions:** Define base instructions for each project to guide LLM responses.


## Tech Stack

### Frontend

- **Next.js (with React):** For building the user interface.
- **TypeScript:** Enhances code quality and developer experience.
- **TanStack Query (React Query):** For efficient data fetching and state management.
- **Shadcn UI:** A collection of re-usable components.

### Backend

- **Python FastAPI:** A modern, fast (high-performance) web framework for building APIs.
- **LangChain:** For LLM orchestration, prompt engineering, and chat history management.

### Database

- **PostgreSQL:** A powerful, open-source relational database.
- **SQLAlchemy:** The Python SQL toolkit and Object Relational Mapper.

### LLM Infrastructure

- **Helicone:** For LLM observability and proxying.
- **Google Gemini:** The underlying LLM provider.

### Authentication

- **NextAuth.js (Auth.js):** For frontend authentication.
- **JWT validation:** Integrated with NextAuth.js for backend API security.
