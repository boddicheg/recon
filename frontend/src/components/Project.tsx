import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  getProjectCommands,
  ProjectCommands,
  addProjectCommand,
} from "../services/Api";

import Command from "./Command";

interface RouteParams {
  [uuid: string]: string | undefined;
}

const Project: React.FC = () => {
  const { uuid } = useParams<RouteParams>();

  const [project, setProject] = useState<ProjectCommands>({
    name: "",
    uuid: "",
    commands: [],
  });

  const [, setLoading] = useState<boolean>(true);
  const [, setError] = useState<string | null>(null);
  const [command, setCommand] = useState<string>("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await addProjectCommand(uuid, command);
      getProjectData(uuid);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred");
      }
    }
  };

  const getProjectData = async (uuid: string | undefined) => {
    try {
      let data = await getProjectCommands(uuid);
      setProject(data);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getProjectData(uuid);
  }, []);

  return (
    <>
      <header className="bg-white shadow">
        <div className="flex flex-row place-content-between mx-auto max-w-7xl px-3 py-3">
          <div>
            <h2 className="text-2xl font-bold tracking-tight text-gray-900">
              Projects / {project.name}
            </h2>
          </div>

          <div>
            <form className="flex space-x-4" onSubmit={handleSubmit}>
              <label
                htmlFor="command"
                className="content-center text-sm font-medium align-middle text-gray-900"
              >
                Command:
              </label>
              <input
                id="command"
                name="command"
                type="text"
                autoComplete="name"
                required
                onChange={(e) => setCommand(e.target.value)}
                className="border rounded-md"
              />

              <button
                type="submit"
                className="rounded-md px-3 py-1 bg-indigo-600 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Add
              </button>
            </form>
          </div>
        </div>
      </header>
      <div>
        <ul role="list" className="flex flex-col divide-y divide-gray-100">
          {project &&
            project.commands &&
            project.commands?.map((command) => (
              <Command uuid={command.uuid} command={command.command}/>
            ))}
        </ul>
      </div>
    </>
  );
};

export default Project;
