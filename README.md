> [!IMPORTANT]
> All pull requests from other branches must be made to the **development** branch before passing it onto the master branch

### Installing Frontend Dependencies

In the frontend folder, ensure all dependencies are installed by running:
```
npm install --legacy-peer-deps
```
### Setting the OpenAI API Key

To set the OpenAI API key, run the following command in your terminal:
```
export OPENAI_API_KEY="your-api-key"
```
### Starting the Server

To start the server, navigate to the backend folder and run the following command:
```
uvicorn main:run_app --host 127.0.0.1 --port 8000 --reload
```
### Starting the Frontend

Finally, navigate to the frontend folder and start the frontend by running:
```
npm run dev
```
