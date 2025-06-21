QualifAIze
==========

QualifAIze is a web application built with Streamlit that provides an automated AI interview system. The app features secure authentication and authorization, enabling users to participate in and manage AI-driven interviews with ease.

Repository: https://github.com/QualifAIze/qualifaize_ui

Features
--------

- Automated AI interview sessions
- Secure authentication and authorization (using python-jose)
- User-friendly UI powered by Streamlit

Getting Started
---------------

1. Clone the repository

   git clone https://github.com/QualifAIze/qualifaize_ui.git
   cd qualifaize_ui

2. Set up the environment (using Miniconda)

   If you don't have Miniconda installed, download it here: https://docs.conda.io/en/latest/miniconda.html

   conda create -n qualifaize python=3.10
   conda activate qualifaize

3. Install dependencies

   pip install -r requirements.txt

4. Run the app

   streamlit run app.py

   (If your main Streamlit file is different, replace `app.py` with the correct file name.)

Configuration
-------------

- The app uses authentication and authorization. Ensure you have any required environment variables or secrets set up (e.g., for JWT tokens, API keys, etc.).
- [List additional setup/config steps here if your app requires specific configs.]

Requirements
------------

- Dependencies are listed in `requirements.txt`:

   requests~=2.32.4
   streamlit~=1.46.0
   python-jose[cryptography]

- As an external service you need `qualifaize_backend_api` which by default runs on port `8080`

License
-------

MIT (or specify your license)


QualifAIze streamlines and automates the interview process, making hiring more efficient and consistent with the power of AI.
