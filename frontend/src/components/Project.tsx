import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { MultiSelect } from "react-multi-select-component";
import {
  getProjectCommands,
  ProjectCommands,
  addProjectCommand,
  sendGetPredefinedCommands,
  GlobalCommands,
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
    target: "",
    commands: [],
  });

  const [, setLoading] = useState<boolean>(true);
  const [, setError] = useState<string | null>(null);
  const [globalCommands, setGlobalCommands] = useState<GlobalCommands>({
    commands: [],
  });
  const [selected, setSelected] = useState([]);
  const [title, setTitle] = useState<string>("");

  const [isCmdGlobal, setIsCmdGlobal] = useState<boolean>(false);

  const handleCheckboxChange = () => {
    setIsCmdGlobal(!isCmdGlobal);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      let selectedCommands: string[] = [];
      selected.map((option) => selectedCommands.push(option["label"]));

      let commandsJoined = selectedCommands.join("\n");
      await addProjectCommand(uuid, commandsJoined, title, isCmdGlobal);
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
      console.log(data);
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

  const getGlobalCommands = async () => {
    try {
      let data = await sendGetPredefinedCommands();
      console.log(data);
      setGlobalCommands(data);
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
    getGlobalCommands();
  }, []);

  const handleDeleteCommand = () => {
    getProjectData(uuid);
  };

  return (
    <>
      <header className="bg-white shadow">
        <div className="flex flex-row place-content-between mx-auto max-w-7xl px-3 py-3 items-center">
          <div>
            <h2 className="text-2xl font-bold tracking-tight text-gray-900">
              Projects / {project.name}
            </h2>
          </div>
          <div>
            <h2 className="text-xl font-bold tracking-tight text-gray-900">
              Target: {project.target}
            </h2>
          </div>
        </div>
        <div className="">
          <form
            className="flex flex-row place-content-between mx-auto max-w-7xl px-3 py-3"
            onSubmit={handleSubmit}
          >
            <MultiSelect
              options={globalCommands.commands}
              value={selected}
              onChange={setSelected}
              labelledBy="Select"
              className="m-2 min-w-80 rounded-md"
              hasSelectAll={false}
              isCreatable={true}
            />
            <input
              id="title"
              name="title"
              type="text"
              required
              onChange={(e) => setTitle(e.target.value)}
              className="m-2 min-w-80 rounded-md"
              placeholder="Command name..."
            />
            <input
              type="checkbox"
              id="exampleCheckbox"
              checked={isCmdGlobal}
              onChange={handleCheckboxChange}
              className="mt-5 mr-2 flex content-center"
            />
            <label htmlFor="exampleCheckbox" className="text-md min-w-64 justify-center content-center">
              Make global
            </label>

            <button
              type="submit"
              className="min-w-24 rounded-md px-4 my-2 mx-2 bg-indigo-600 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              Add
            </button>
          </form>
        </div>
      </header>
      <div>
        <ul role="list" className="flex flex-col divide-y divide-gray-100">
          {project &&
            project.commands &&
            project.commands?.map((command) => (
              <Command
                uuid={command.uuid}
                command={command.command}
                title={command.title}
                onDelete={handleDeleteCommand}
              />
            ))}
        </ul>
      </div>
    </>
  );
};

export default Project;
