import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  getProjectCommands,
  ProjectCommands,
  addProjectCommand,
  startCommandExecution,
  stopCommandExecution,
  deleteCommandData,
} from "../services/Api";

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

  const startCommandProcessing = async (cmd_uuid: string | undefined) => {
    // console.log("[startCommandProcessing] ", cmd_uuid, ", parent: ", uuid);
    await startCommandExecution(cmd_uuid);
  };

  const stopCommandProcessing = async (cmd_uuid: string | undefined) => {
    // console.log("[stopCommandProcessing] ", cmd_uuid, ", parent: ", uuid);
    await stopCommandExecution(cmd_uuid);
  };

  const deleteCommand = async (cmd_uuid: string | undefined) => {
    // console.log("[deleteCommand] ", cmd_uuid, ", parent: ", uuid);
    await deleteCommandData(cmd_uuid);
  };

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
                className="text-sm font-medium align-middle text-gray-900"
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
              <li className="gap-x-6 py-1 px-1 my-2 border border-slate-100 bg-slate-50 shadow-md rounded hover:shadow-lg cursor-pointer">
                <div className="flex gap-x-4 justify-between">
                  <div className="flex-none min-w-0 content-center ml-2">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth={1.5}
                      stroke="currentColor"
                      className="size-8 stroke-indigo-700"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="m6.75 7.5 3 2.25-3 2.25m4.5 0h3m-9 8.25h13.5A2.25 2.25 0 0 0 21 18V6a2.25 2.25 0 0 0-2.25-2.25H5.25A2.25 2.25 0 0 0 3 6v12a2.25 2.25 0 0 0 2.25 2.25Z"
                      />
                    </svg>
                  </div>
                  <div className="flex-none min-w-0">
                    <p className="text-lg leading-6 text-gray-900">
                      Command:{" "}
                      <span className="font-bold">{command.command}</span>
                    </p>
                    <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                      Added: 123
                    </p>
                  </div>
                  <div className="flex-1 content-center  mr-4">
                    <div className="flex justify-end gap-x-4">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={1.5}
                        stroke="currentColor"
                        className="size-6"
                        onClick={() => startCommandProcessing(command.uuid)}
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z"
                        />
                      </svg>
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={1.5}
                        stroke="currentColor"
                        className="size-6"
                        onClick={() => stopCommandProcessing(command.uuid)}
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
                        />
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M9 9.563C9 9.252 9.252 9 9.563 9h4.874c.311 0 .563.252.563.563v4.874c0 .311-.252.563-.563.563H9.564A.562.562 0 0 1 9 14.437V9.564Z"
                        />
                      </svg>
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={1.5}
                        stroke="currentColor"
                        className="size-6"
                        onClick={() => deleteCommand(command.uuid)}
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
                        />
                      </svg>
                    </div>
                  </div>
                </div>
                <div className="flex">
                  <div className="flex-1 mr-4 ml-4">
                    {command.output != "" ? (
                      <div id={"output-" + command.uuid} className="col-span-2">
                        {command.output}
                      </div>
                    ) : null}
                  </div>
                </div>
              </li>
            ))}
        </ul>
      </div>
    </>
  );
};

export default Project;
