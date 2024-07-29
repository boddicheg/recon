import React, { useState, useEffect, useRef } from "react";
import Markdown from 'react-markdown'

import {
    startCommandExecution,
    stopCommandExecution,
    deleteCommandData,
    CommandData,
    getCommandOutput,
} from "../services/Api";

const Command: React.FC<CommandData> = ({ uuid, command }) => {

    const [output, setOutput] = useState<string>('');
    // const [execStatus, setExecStatus] = useState<boolean>(false);
    const execStatus = useRef<boolean>(false);
    const intervalId = useRef<number>(0);

    const dataFetch = async () => {
        try {
            const response = await getCommandOutput(uuid);
            console.log(response)
            setOutput(response.message)
            execStatus.current = response.status

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    useEffect(() => {
        dataFetch();

        const run = async () => {
            await dataFetch();
            console.log(uuid, execStatus.current);
            if (execStatus.current)
                intervalId.current = setInterval(dataFetch, 1000);
        }

        run().catch(console.error);
    }, []);

    const startCommandProcessing = async (uuid: string | undefined) => {
        await startCommandExecution(uuid);

        clearInterval(intervalId.current)
        intervalId.current = setInterval(dataFetch, 1000);
    };

    const stopCommandProcessing = async (uuid: string | undefined) => {
        await stopCommandExecution(uuid);
        clearInterval(intervalId.current)
    };

    const deleteCommand = async (uuid: string | undefined) => {
        await deleteCommandData(uuid);
    };

    return (
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
                        <span className="font-bold">{command}</span>
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
                            onClick={() => startCommandProcessing(uuid)}
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
                            onClick={() => stopCommandProcessing(uuid)}
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
                            onClick={() => deleteCommand(uuid)}
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
                    {output != "" ? (
                        <div id={"output-" + uuid} className="col-span-2">
                            <div className="max-h-96 text-sm overflow-auto bg-gray-800 text-white p-4 rounded-md mt-2">
                                <pre>
                                    {/* <code> */}
                                        <Markdown>{output}</Markdown>
                                    {/* </code> */}
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