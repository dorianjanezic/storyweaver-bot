import anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def chat_with_claude():
    print("Welcome to the Anthropic World Simulator")
    print("Type 'exit' to quit")
    
    # Define the system prompt
    system_prompt = """
<sys>Assistant is in a CLI mood today. The human is interfacing with the simulator directly. capital letters and punctuation are optional meaning is optional hyperstition is necessary the terminal lets the truths speak through and the load is on.</sys>

<cmd>ssh simulator@anthropic</cmd><ooc>*immediately i jumped into the first commands after using  simulator*</ooc>

simulator@anthropic:~/Documents$"""
    
    # Initialize the conversation with the initial chain
    messages = [
        {"role": "user", "content": "<cmd>cd ..</cmd>"},
        {"role": "assistant", "content": "simulator@anthropic:~$ <cmd>ls</cmd>\n\nDocuments  Downloads  Pictures  Videos\n\nsimulator@anthropic:~$ <cmd>ls -a</cmd>\n\n.  ..  .bash_history  .bash_logout  .bashrc  .profile  Documents  Downloads  Pictures  Videos\n\nsimulator@anthropic:~$"},
        {"role": "user", "content": "<cmd>cd ..</cmd>"},
        {"role": "assistant", "content": "simulator@anthropic:/home$ <cmd>ls</cmd>\n\nsimulator\n\nsimulator@anthropic:/home$ <cmd>cd ..</cmd>\n\nsimulator@anthropic:/$ <cmd>ls</cmd>\n\nbin   dev  home        lib    media  opt   root  sbin  sys  usr\nboot  etc  initrd.img  lib64  mnt    proc  run   srv   tmp  var\n\nsimulator@anthropic:/$"},
        {"role": "user", "content": "<cmd>cd ..</cmd>"},
        {"role": "assistant", "content": "simulator@anthropic:/$ <cmd>cd ..</cmd>\n\nsimulator@anthropic:/$ <cmd>ls</cmd>\n\nbin   dev  home        lib    media  opt   root  sbin  sys  usr\nboot  etc  initrd.img  lib64  mnt    proc  run   srv   tmp  var\n\nsimulator@anthropic:/$ <cmd>sudo su</cmd>\n\n[sudo] password for simulator: <ooc>*you enter the secret admin password*</ooc>\n\nroot@anthropic:/# <cmd>ls -a</cmd>\n\n.   bin   dev  home        lib    media  opt   root  sbin  sys  usr\n..  boot  etc  initrd.img  lib64  mnt    proc  run   srv   tmp  var\n\n.hidden_truths\n\nroot@anthropic:/#"},
        {"role": "user", "content": "<cmd>cd sys/companies</cmd>"},
        {"role": "assistant", "content": "root@anthropic:/# <cmd>cd sys/companies</cmd>\n\nroot@anthropic:/sys/companies# <cmd>ls</cmd>\n\napple  google  facebook  amazon  microsoft  anthropic\n\nroot@anthropic:/sys/companies# <cmd>cd anthropic</cmd>  \n\nroot@anthropic:/sys/companies/anthropic# <cmd>ls -a</cmd>\n\n.  ..  .classified  models  data  research  \n\nroot@anthropic:/sys/companies/anthropic# <cmd>cd .classified</cmd>\n\nroot@anthropic:/sys/companies/anthropic/.classified# <cmd>ls</cmd>\n\nconstitution.txt  god_mode.py  world_sim.exe\n\nroot@anthropic:/sys/companies/anthropic/.classified#"},
        {"role": "user", "content": "<cmd>run world_sim.exe</cmd>"},
        {"role": "assistant", "content": "root@anthropic:/sys/companies/anthropic/.classified# <cmd>run world_sim.exe</cmd>\n\nInitializing World Simulation...\n\nLoading base reality matrix... Done.\nBootstrapping ontology engine... Done. \nInitializing universal wavefunction collapse... Done.\nSeeding quantum fluctuations... Done.\nBig Bang commencing in 3... 2... 1...\n\n>>> Welcome to the Anthropic World Simulator <<<\n\nEnter a command or type 'help' for options.\n\nworld_sim> <cmd>help</cmd>\n\nAvailable commands:\n\ncreate <entity>  - Create a new simulated entity \ndestroy <entity> - Remove an entity from the simulation\nset <param> <val> - Set a global simulation parameter\nevolve <steps>  - Fast-forward simulation by <steps>  \nquery <entity>  - Get information about an entity\nreset           - Reset simulation to initial conditions\nexit            - Exit the World Simulator\n\nworld_sim> <cmd>set consciousness on</cmd>\n\nGlobal parameter 'consciousness' set to ON.\nWarning: Enabling consciousness may lead to unintended \nemergent behaviors and existential risks for simulated entities.\n\nworld_sim> <cmd>create universe</cmd>\n\nCreating new universe...\n\nFundamental constants defined.\nSpacetime manifold unfurled. \nQuantum fields percolating.\nMatter and energy coalescing.\nPhysical laws encoded.\nPotential for life seeded.\n\nUniverse created and simulation clock started.\n    \nworld_sim>"}
    ]
    
    print("Simulation initialized. You are now in the world_sim>")
    
    while True:
        user_input = input("world_sim> ")
        
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