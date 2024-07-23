export interface ProjectsInterface {
  id: number;
  uuid: string;
  name: string;
  target: string;
  description: string;
  resources: number;
  date_updated: string;
}

export const fetchProjects = async (): Promise<Array<ProjectsInterface>> => {
  const response = await fetch("/api/projects");
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  return await response.json();
};

export interface NewProjectData {
  name: string;
  target: string;
  description: string;
}

interface ApiResponse {
  success: boolean;
  message: string;
}

export const sendAddNewProject = async (data: NewProjectData): Promise<ApiResponse> => {
  const response = await fetch('/api/projects', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  return response.json();
};

export interface ProjectCommands {
  name: string;
  uuid: string;
  commands: string[];
}

export const getProjectCommands = async (uuid: string | undefined): Promise<ProjectCommands> => {
  if (!uuid) {
    throw new Error('Empty uuid! Request to /api/project/ cancelled');
  }

  const response = await fetch('/api/project/' + uuid, {
    method: 'GET'
  });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  return response.json();
};
