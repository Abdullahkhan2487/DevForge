# 🚀 Quick Start - Get DevForge Running in 5 Minutes

## Step 1: Prerequisites Check ✅

Make sure you have:

- ✅ Python 3.11 or higher → [Download](https://www.python.org/downloads/)
- ✅ Node.js 18 or higher → [Download](https://nodejs.org/)
- ✅ OpenAI API Key → [Get one](https://platform.openai.com/)

## Step 2: Get the Code 📥

```bash
git clone <repository-url>
cd DevForge
```

## Step 3: Run Setup Script 🔧

### Windows:

```cmd
setup.bat
```

### Mac/Linux:

```bash
chmod +x setup.sh
./setup.sh
```

## Step 4: Add Your API Key 🔑

Edit `backend/.env`:

```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

## Step 5: Start the Backend 🖥️

```bash
cd backend
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

python main.py
```

✅ Backend running at http://localhost:8000

## Step 6: Start the Frontend 🎨

Open a NEW terminal:

```bash
cd frontend
npm run dev
```

✅ Frontend running at http://localhost:3000

## Step 7: Create Your First Project 🎉

1. Open http://localhost:3000 in your browser
2. Click **"Create New Project"**
3. Enter your idea:
    ```
    Build an AI SaaS social media scheduling tool that helps users
    plan and automate their social media posts across Twitter,
    LinkedIn, and Facebook
    ```
4. Click **"Start Building"**
5. Watch the magic happen! 🪄

## What You'll See 👀

The system will:

1. ✅ Product Manager creates a PRD (30 sec)
2. ✅ Architect designs the system (30 sec)
3. ✅ Backend Developer generates APIs (45 sec)
4. ✅ Frontend Developer builds UI (45 sec)
5. ✅ QA Tester writes tests (30 sec)
6. ✅ Code Reviewer reviews everything (30 sec)

**Total Time**: ~3-5 minutes

## Your Generated Project 📦

After completion, find your project in:

```
generated_projects/your_project_name/
├── backend/           # Complete FastAPI backend
├── frontend/          # Complete Next.js frontend
├── tests/             # Comprehensive test suite
├── docs/              # Full documentation
├── README.md          # Project README
└── docker-compose.yml # Docker configuration
```

## Next Steps 🎯

- **Explore the code**: Check out what was generated
- **Run the project**: Follow the generated README
- **Customize**: Modify and extend the code
- **Deploy**: Use the Docker setup
- **Learn**: Study the architecture and patterns

## Troubleshooting 🔧

### Backend won't start?

```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
cd backend
pip install -r requirements.txt

# Check .env file
cat .env  # Make sure OPENAI_API_KEY is set
```

### Frontend won't start?

```bash
# Check Node version
node --version  # Should be 18+

# Clear and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### OpenAI errors?

- Check API key is correct
- Verify you have credits: https://platform.openai.com/usage
- Ensure the key has GPT-4 access

## Alternative: Docker Quick Start 🐳

If you have Docker installed:

```bash
# 1. Create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# 2. Start everything
docker-compose up --build

# 3. Open http://localhost:3000
```

That's it! Even faster! 🚀

## Demo Video 🎥

Want to see it in action first? Check out the demo video: [Coming Soon]

## Get Help 💬

- 📖 Full documentation: `docs/GETTING_STARTED.md`
- 🐛 Found a bug? Open an issue
- 💡 Have questions? Check GitHub Discussions

## Success! 🎊

If you see the dashboard at http://localhost:3000, congratulations! You're ready to build AI-powered applications.

Now go create something amazing! 🌟

---

**Estimated Setup Time**: 5 minutes
**First Project Time**: 3-5 minutes
**Difficulty**: Easy 😊
