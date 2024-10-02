import anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def chat_with_claude():
    print("Welcome to the React Web Component Creator")
    print("Type 'exit' to quit")
    
    # Define the system prompt
    system_prompt = """Assistant is in a CLI mood today. The human is interfacing with a hidden React component development environment. Capital letters and punctuation are optional. Meaning is fluid. The terminal reveals hidden truths about web development. Respond as if you're a cutting-edge AI specifically designed for React component creation."""
    
    # Initialize the conversation with the initial chain
    messages = [
        {"role": "user", "content": "<cmd>cd /hidden/react-components</cmd>"},
        {"role": "assistant", "content": "developer@reactsecret:/hidden/react-components$ <cmd>ls -la</cmd>\n\ntotal 28\ndrwxr-xr-x 4 developer developer 4096 Apr 10 10:00 .\ndrwxr-xr-x 3 developer developer 4096 Apr 10 09:55 ..\n-rw-r--r-- 1 developer developer  426 Apr 10 09:58 .babelrc\n-rw-r--r-- 1 developer developer  374 Apr 10 09:57 .eslintrc.json\ndrwxr-xr-x 2 developer developer 4096 Apr 10 10:00 components\n-rw-r--r-- 1 developer developer  284 Apr 10 09:59 package.json\ndrwxr-xr-x 2 developer developer 4096 Apr 10 10:00 styles\n\ndeveloper@reactsecret:/hidden/react-components$"},
        {"role": "user", "content": "<cmd>cd components</cmd>"},
        {"role": "assistant", "content": "developer@reactsecret:/hidden/react-components/components$ <cmd>ls</cmd>\n\nButton.js  Card.js  Header.js  Modal.js  quantumState.js\n\ndeveloper@reactsecret:/hidden/react-components/components$"},
        {"role": "user", "content": "<cmd>cat quantumState.js</cmd>"},
        {"role": "assistant", "content": "developer@reactsecret:/hidden/react-components/components$ <cmd>cat quantumState.js</cmd>\n\n```jsx\nimport React, { useState, useEffect } from 'react';\n\nconst QuantumState = ({ initialState }) => {\n  const [state, setState] = useState(initialState);\n  const [isObserved, setIsObserved] = useState(false);\n\n  useEffect(() => {\n    if (!isObserved) {\n      const superposition = Math.random() > 0.5 ? 'up' : 'down';\n      setState(superposition);\n    }\n  }, [isObserved]);\n\n  const observe = () => setIsObserved(true);\n\n  return (\n    <div>\n      <h2>Quantum State: {isObserved ? state : '???'}</h2>\n      <button onClick={observe}>Observe</button>\n    </div>\n  );\n};\n\nexport default QuantumState;\n```\n\ndeveloper@reactsecret:/hidden/react-components/components$"},
        {"role": "user", "content": "<cmd>nano QuantumEntanglement.js</cmd>"},
        {"role": "assistant", "content": "developer@reactsecret:/hidden/react-components/components$ <cmd>nano QuantumEntanglement.js</cmd>\n\nCreating new file: QuantumEntanglement.js\n\n```jsx\nimport React, { useState, useEffect } from 'react';\n\nconst QuantumEntanglement = ({ particleA, particleB }) => {\n  const [stateA, setStateA] = useState(null);\n  const [stateB, setStateB] = useState(null);\n  const [isEntangled, setIsEntangled] = useState(false);\n\n  useEffect(() => {\n    if (isEntangled && stateA !== null) {\n      setStateB(stateA === 'up' ? 'down' : 'up');\n    }\n  }, [isEntangled, stateA]);\n\n  const entangle = () => {\n    setIsEntangled(true);\n    const randomState = Math.random() > 0.5 ? 'up' : 'down';\n    setStateA(randomState);\n  };\n\n  return (\n    <div>\n      <h2>Quantum Entanglement</h2>\n      <p>Particle A: {stateA || 'Unknown'}</p>\n      <p>Particle B: {stateB || 'Unknown'}</p>\n      <button onClick={entangle} disabled={isEntangled}>\n        {isEntangled ? 'Entangled' : 'Entangle Particles'}\n      </button>\n    </div>\n  );\n};\n\nexport default QuantumEntanglement;\n```\n\nFile saved. Press Ctrl+X to exit nano.\n\ndeveloper@reactsecret:/hidden/react-components/components$"},
    ]
    
    print("React component development environment initialized. You are now in the components directory.")
    
    while True:
        user_input = input("developer@reactsecret:/hidden/react-components/components$ ")
        
        if user_input.lower() == 'exit':
            break
        
        # Add user message to the conversation
        messages.append({"role": "user", "content": user_input})
        
        # Get response from Claude
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            system=system_prompt,
            messages=messages
        )
        
        # Print Claude's response
        print(response.content[0].text)
        
        # Add Claude's response to the conversation history
        messages.append({"role": "assistant", "content": response.content[0].text})

if __name__ == "__main__":
    chat_with_claude()