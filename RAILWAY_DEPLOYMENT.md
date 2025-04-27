# Deploying Asha AI Chatbot to Railway

## Prerequisites
- A [Railway](https://railway.app/) account
- [Railway CLI](https://docs.railway.app/develop/cli) installed (optional)

## Deployment Steps

### Option 1: Using Railway Dashboard (Recommended for beginners)

1. Log in to your [Railway Dashboard](https://railway.app/dashboard)

2. Click on "New Project" and select "Deploy from GitHub repo"

3. Select your GitHub repository (you may need to connect your GitHub account first)

4. Configure the deployment settings:
   - Railway will automatically detect this as a Python project
   - Environment variables: Add any necessary API keys (like your Groq API key)

5. Click "Deploy" and wait for the build to complete

6. Once deployed, Railway will provide you with a public URL for your application

### Option 2: Using Railway CLI

1. Make sure you're in the root directory of your project:
   ```
   cd asha_ai_chatbot
   ```

2. Log in to Railway:
   ```
   railway login
   ```

3. Initialize a new Railway project:
   ```
   railway init
   ```

4. Link your project:
   ```
   railway link
   ```

5. Deploy your project:
   ```
   railway up
   ```

6. Open your deployed application:
   ```
   railway open
   ```

## Environment Variables

Make sure to set these environment variables in your Railway project settings:

- `GROQ_API_KEY`: Your Groq API key (if using Groq API)
- Any other API keys or configuration needed by your application

## Continuous Deployment

Railway automatically sets up continuous deployment from your GitHub repository. Any changes pushed to your main branch will trigger a new deployment.

## Monitoring and Logs

You can monitor your application and view logs in the Railway dashboard under the "Deployments" tab.

## Troubleshooting

If you encounter any issues:

1. Check your application logs in the Railway dashboard
2. Verify your environment variables are correctly set
3. Make sure your `railway.toml` and `Procfile` are in the root directory
4. If needed, try deploying with debug mode enabled temporarily 