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
  status: boolean;
  message: string;
}

export const sendAddNewProject = async (
  data: NewProjectData
): Promise<ApiResponse> => {
  const response = await fetch("/api/projects", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  return response.json();
};

export interface CommandData {
  uuid: string;
  command: string;
}

export interface ProjectCommands {
  name: string;
  uuid: string;
  commands: CommandData[];
}

export const getProjectCommands = async (
  uuid: string | undefined
): Promise<ProjectCommands> => {
  if (!uuid) {
    throw new Error("Empty uuid! Request to /api/project/ cancelled");
  }

  const response = await fetch("/api/project/" + uuid, {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  return response.json();
};

export const addProjectCommand = async (
  uuid: string | undefined,
  command: string
): Promise<ApiResponse> => {
  const response = await fetch("/api/project/" + uuid, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({command: command}),
  });

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  return response.json();
};

export const startCommandExecution = async (
  uuid: string | undefined
): Promise<ApiResponse> => {
  if (!uuid) {
    throw new Error("Empty uuid! Request to /api/command/ cancelled");
  }

  const response = await fetch("/api/command/" + uuid + "/start", {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  return response.json();
}

export const stopCommandExecution = async (
  uuid: string | undefined
): Promise<ApiResponse> => {
  if (!uuid) {
    throw new Error("Empty uuid! Request to /api/command/ cancelled");
  }

  const response = await fetch("/api/command/" + uuid + "/stop", {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  return response.json();
}

export const deleteCommandData = async (
  uuid: string | undefined
): Promise<ApiResponse> => {
  if (!uuid) {
    throw new Error("Empty uuid! Request to /api/command/ cancelled");
  }

  const response = await fetch("/api/command/" + uuid, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  return response.json();
}


export interface CommandOutput {
  output: string
}

export const getCommandOutput = async (
  uuid: string | undefined
): Promise<ApiResponse> => {
  if (!uuid) {
    throw new Error("Empty uuid! Request to /api/command/<uuid>/output cancelled");
  }

  const response = await fetch("/api/command/" + uuid + "/output", {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  return response.json();
};