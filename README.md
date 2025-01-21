# AI Photo Description Generator

A Flask application that generates natural language descriptions for uploaded photos using OpenAI's Vision API.

⚠️ **IMPORTANT SECURITY NOTE**: This is a public repository. Never commit sensitive information like API keys, passwords, or personal data. Always use environment variables for secrets.

## Prerequisites

- Python 3.8+
- OpenAI API key
- Git

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/pkrzekotowski/ai-photo-description.git
cd ai-photo-description
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
cd app
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Edit `.env` and add your OpenAI API key.

5. Run the application:
```bash
python app.py
```

## Deployment Options

### Option 1: Deploy to Render

1. Create a [Render](https://render.com) account if you don't have one.

2. Create a new Web Service:
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - Name: `ai-photo-description` (or your preferred name)
     - Environment: `Python 3`
     - Build Command: `pip install -r app/requirements.txt`
     - Start Command: `cd app && python app.py`
     - Select the branch to deploy

3. Add environment variables:
   - Go to "Environment" tab
   - Add `OPENAI_API_KEY` with your API key

4. Deploy:
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

### Option 2: Deploy to AWS Elastic Beanstalk

1. Install AWS CLI and EB CLI:
```bash
pip install awscli awsebcli
```

2. Configure AWS credentials:
```bash
aws configure
```

3. Initialize Elastic Beanstalk:
```bash
eb init -p python-3.8 ai-photo-description --region us-east-1
```

4. Create the environment:
```bash
eb create ai-photo-description-env
```

5. Set environment variables:
```bash
eb setenv OPENAI_API_KEY=your_api_key_here
```

6. Deploy:
```bash
eb deploy
```

7. Open the application:
```bash
eb open
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Project Structure

```
ai-photo-description/
├── app/
│   ├── app.py           # Main Flask application
│   ├── config.py        # Configuration settings
│   ├── requirements.txt # Python dependencies
│   ├── templates/       # HTML templates
│   └── .env            # Environment variables (not in git)
└── README.md
```

## Security Notes

- ⚠️ This is a public repository - be extra careful with sensitive data
- Never commit `.env` files containing sensitive information
- Always use environment variables for API keys and secrets
- Keep your OpenAI API key secure and rotate it if compromised
- If you accidentally commit sensitive data:
  1. Immediately revoke/rotate the exposed credentials
  2. Contact GitHub support to purge the sensitive data
  3. Use `git filter-branch` or BFG Repo Cleaner to remove secrets from history

## Troubleshooting

1. If the application fails to start:
   - Check if all environment variables are set correctly
   - Verify Python version compatibility
   - Ensure all dependencies are installed

2. If image uploads fail:
   - Check file size limits
   - Verify supported image formats (PNG, JPEG, WebP)

3. For deployment issues:
   - Check deployment logs
   - Verify environment variables are set in the deployment platform
   - Ensure all requirements are properly installed

## Contributing

We welcome contributions! Please follow these steps:

1. Check existing issues or create a new one to discuss your proposed changes
2. Fork the repository
3. Create a feature branch (`git checkout -b feature/amazing-feature`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Code of Conduct

- Be respectful and inclusive
- Follow the existing code style
- Write clear commit messages
- Add tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License.
