function App() {
    const projectName = "{{cookiecutter.project_name}}";

    return (
        <main>
            <h1>{projectName}</h1>
            <p>AI Engineering Application</p>
        </main>
    );
}

export default App;