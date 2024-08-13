from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import mimetypes
import datetime

from proejcts import *

# Very important "fix" for sending js as text/javascript, not like text/plain
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/javascript', '.js')

app = Flask(__name__, static_folder='static/assets', static_url_path='/assets')
root = os.path.dirname(os.path.abspath(__file__))
fronend_path = f"{root}/annotate-app/dist"

g_projects = ProjectsController(root)

@app.route('/', methods=['GET'])
def index():
    return render_template(f'index.html')

@app.route('/api/ver', methods=['GET'])
def api():
    return jsonify({
        'message': 'v0.0.1', 
    }), 200

@app.route('/api/projects', methods=['GET'])
def api_projects_get():
    return jsonify(g_projects.get_projects()), 200

@app.route('/api/projects', methods=['POST'])
def api_projects_add():
    data = request.get_json()
    
    g_projects.add_project(data)
    
    return jsonify({
        "message": "Added successfully"
    }), 200

@app.route('/api/project/<uuid>', methods=['GET'])
def api_project_get_cmds(uuid):
    commands = g_projects.get_project_cmds(uuid)
    project = g_projects.get_project(uuid)
    
    if not project:
        return {}

    return jsonify({
        "name": project["name"],
        "uuid": project["uuid"],
        "target": project["target"],
        "commands": commands
    }), 200

@app.route('/api/project/<uuid>', methods=['POST'])
def api_project_add_cmd(uuid):
    print(request.get_json())
    if "title" in request.get_json().keys() and \
        "command" in request.get_json().keys() and \
        "is_global" in request.get_json().keys():
        g_projects.add_command(uuid, 
                               request.get_json()["command"],
                               request.get_json()["title"],
                               request.get_json()["is_global"])
    
    return jsonify({
        "message": "Added successfully"
    }), 200

@app.route('/api/command/<uuid>/start', methods=['GET'])
def api_project_cmd_start(uuid):
    g_projects.start_execution(uuid)
    return jsonify({
        "message": f"{uuid} started successfully"
    }), 200
    
@app.route('/api/command/<uuid>/stop', methods=['GET'])
def api_project_cmd_stop(uuid):
    g_projects.stop_execution(uuid)
    return jsonify({
        "message": f"{uuid} stopped successfully"
    }), 200

@app.route('/api/command/<uuid>/output', methods=['GET'])
def api_project_cmd_output(uuid):
    return jsonify({
        "message": g_projects.get_output(uuid),
        "status": g_projects.get_status(uuid)
    }), 200
    
@app.route('/api/command/global', methods=['GET'])
def api_project_cmd_global():
    cmds = g_projects.get_global_cmds()
    return jsonify({
        "commands": cmds
    }), 200

@app.route('/api/command/<uuid>', methods=['DELETE'])
def api_project_cmd_delete(uuid):
    g_projects.detete_command(uuid)
    return jsonify({
        "message": f"{uuid} deleted successfully"
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3333)