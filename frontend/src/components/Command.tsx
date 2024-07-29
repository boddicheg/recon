import React, { useState, useEffect, useRef } from "react";
import {
  PlayIcon,
  StopIcon,
  TrashIcon,
  CommandLineIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  ArrowPathIcon
} from "@heroicons/react/24/outline";
import {
  startCommandExecution,
  stopCommandExecution,
  deleteCommandData,
  CommandData,
  getCommandOutput,
} from "../services/Api";

const Command: React.FC<CommandData> = ({ uuid, command, onDelete }) => {
  const [output, setOutput] = useState<string>("");
  const [toggleStatus, setToggleStatus] = useState<boolean>(false);
  const execStatus = useRef<boolean>(false);
  const intervalId = useRef<number>(0);
  const codeBoxRef = useRef<HTMLDivElement>(null);

  const dataFetch = async () => {
    try {
      const response = await getCommandOutput(uuid);
      console.log(response);
      setOutput(response.message);
      execStatus.current = response.status;

      setToggleStatus(response.message != "");

      if (codeBoxRef.current) {
        codeBoxRef.current.scrollTop = 9999; // codeBoxRef.current.scrollHeight;
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    dataFetch();

    const run = async () => {
      await dataFetch();
      if (execStatus.current) intervalId.current = setInterval(dataFetch, 1000);
      else clearInterval(intervalId.current);
    };

    run().catch(console.error);

    setToggleStatus(false);
  }, []);

  const startCommandProcessing = async (uuid: string | undefined) => {
    await startCommandExecution(uuid);

    clearInterval(intervalId.current);
    intervalId.current = setInterval(dataFetch, 1000);
  };

  const stopCommandProcessing = async (uuid: string | undefined) => {
    await stopCommandExecution(uuid);
    clearInterval(intervalId.current);
  };

  const deleteCommand = async (uuid: string | undefined) => {
    await deleteCommandData(uuid);
    onDelete();
  };

  const toggleOutput = () => {
    setToggleStatus(!toggleStatus);
    console.log("Set toggle to ", toggleStatus);
  };

  return (
    <li className="gap-x-6 py-1 px-1 my-2 border border-slate-100 bg-slate-50 shadow-md rounded hover:shadow-lg cursor-pointer">
      <div className="flex gap-x-4 justify-between">
        <div className="flex-none min-w-0 content-center ml-2">
          <CommandLineIcon className="size-8 stroke-indigo-700" />
        </div>
        <div className="flex-none min-w-0">
          <p className="text-lg leading-6 text-gray-900">
            Command: <span className="font-bold">{command}</span>
          </p>
          <p className="mt-1 truncate text-xs leading-5 text-gray-500">
            Added: 123
          </p>
        </div>
        <div className="flex-1 content-center  mr-4">
          <div className="flex justify-end gap-x-4">
            {execStatus.current ? (
              <ArrowPathIcon 
                className="size-6 animate-spin"
              />
            ): null}

            <PlayIcon
              className="size-6 fill-green-400 stroke-green-600"
              onClick={() => startCommandProcessing(uuid)}
            />
            <StopIcon
              className="size-6 fill-red-400 stroke-red-600"
              onClick={() => stopCommandProcessing(uuid)}
            />
            <TrashIcon
              className="size-6 fill-gray-400 stroke-gray-600"
              onClick={() => deleteCommand(uuid)}
            />
            {!toggleStatus ? (
              <ChevronDownIcon
                className="size-6"
                onClick={() => toggleOutput()}
              />
            ) : null}
            {toggleStatus ? (
              <ChevronUpIcon
                className="size-6"
                onClick={() => toggleOutput()}
              />
            ) : null}
          </div>
        </div>
      </div>
      <div className="flex">
        <div className="flex-1 mr-4 ml-4">
          {toggleStatus ? (
            <div id={"output-" + uuid} className="col-span-2">
              <div
                ref={codeBoxRef}
                className="max-h-96 text-sm overflow-auto bg-gray-800 text-white p-4 rounded-md mt-2"
              >
                <pre>
                  {/* <Markdown>{output}</Markdown> */}
                  {output}
                </pre>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </li>
  );
};

export default Command;
