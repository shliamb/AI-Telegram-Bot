# Base:
# import aiohttp
# from setup_config_logger import setup_logger
# logger_ai = setup_logger('ai', f'{PATH_LOGS}ai.log')
# import json
# from typing import Dict, Optional, Any, List
# import asyncio
#System:
#from get_keys import USERNAME_API_AI, KEY_API_AI, VALUE_KEY_API_AI
#from config import URL, LIST_ASSIST_OA, DEL_ASSIST_OA, DEL_THREAD_OA, RETRIEVE_OA, RUN_ASSIST_CUSTOM_0525, RETUEN_RESULT_OA




# class AssistOpenAI:
#     '''
#     Обращение к API AI Proxy OpenAI Assistent
#     '''
#     def __init__(self):
#         self.url = URL
#         self.data = {"username": USERNAME_API_AI}
#         self.headers = {KEY_API_AI: VALUE_KEY_API_AI}

#     # Отправка данных на API и получение :
#     async def assis_post(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
#         """
#         Send data to API and receive response
        
#         Args:
#             url: endpoint URL
#             data: request data
            
#         Returns:
#             Dictionary with response data or error info
#         """
#         async with aiohttp.ClientSession() as session:
#             async with session.post(url, headers=self.headers, data=data) as response:
#                 if response.status == 200:
#                     return await response.json()
#                 content = await response.text()
#                 logging.error(f"Status (статус): {response.status}, Error: {content}")
#                 return {"status": response.status, "error": content}


#     # Получение списка Ассистентов:
#     async def list_assist_oa(self) -> Dict[str, Any]:
#         """Get list of Assistants"""
#         url = f"{self.url}{LIST_ASSIST_OA}"
#         return await self.assis_post(url, self.data)


#     # Удаление Ассистента по его id:
#     async def del_assist_oa(self, assistant_id: str) -> Dict[str, Any]:
#         """
#         Delete Assistant by ID
        
#         Args:
#             assistant_id: ID of the assistant to delete
#         """
#         url = f"{self.url}{DEL_ASSIST_OA}"
#         data = {**self.data, "assistant_id": assistant_id} # Старый вариант - data = self.data.copy()  data["thread_id"] = thread_id 
#         return await self.assis_post(url, data)


#     # Удаление Тред по его id:
#     async def del_thread_oa(self, thread_id: str) -> Dict[str, Any]:
#         """
#         Delete Thread by ID
        
#         Args:
#             thread_id: ID of the thread to delete
#         """
#         url = f"{self.url}{DEL_THREAD_OA}"
#         data = {**self.data, "thread_id": thread_id}
#         return await self.assis_post(url, data)


#     # Получение ответа от активного Ассист по каналу и индетификатору запуска:
#     async def get_retrieve_oa(self, thread_id: str, run_id: str) -> Dict: # status, tool_calls
#         """
#         Get response from active Assistant by thread and run ID
        
#         Args:
#             thread_id: Thread identifier
#             run_id: Run identifier

#         Answer:
#             Tuple: status, tool_calls
#         """
#         url = f"{self.url}{RETRIEVE_OA}"
#         data = {**self.data, "thread_id": thread_id, "run_id": run_id}
#         return await self.assis_post(url, data)


#     # Отправка результата Ассистенту:
#     async def returning_result_assist_oa(self, thread_id: str, run_id: str, tool_outputs: List):
#         """
#         Возвращает результат Ассистенту
#         tool_outputs - список сформированных при работе функций результатов
        
#         Args:
#             thread_id: Thread identifier
#             run_id: Run identifier
#             tool_outputs:
#             tool_outputs=[
#                 {
#                     "tool_call_id": "435353",
#                     "output": "15"
#                 },
#                 {
#                     "tool_call_id": "3565464",
#                     "output": None
#                 }
#             ]

#         """
#         url = f"{self.url}{RETUEN_RESULT_OA}"
#         data = {**self.data, "thread_id": thread_id, "run_id": run_id, "tool_outputs": json.dumps(tool_outputs, ensure_ascii=False)} 
#         return await self.assis_post(url, data)


#     # Запуск Ассистента по assistant_id и thread_id, если нет - создает:
#     async def run_custom_assist_0525_oa(
#         self, 
#         thread_id: Optional[str] = None, 
#         assistant_id: Optional[str] = None, 
#         instructions: Optional[str] = None, 
#         model: Optional[str] = None, 
#         user_content: Optional[str] = None, 
#         tools: Optional[List[Dict[str, Any]]] = None
#     ) -> Dict[str, Any]:
#         """
#         Run Assistant by parameters, creates thread if needed
        
#         Args:
#             thread_id: Optional thread ID
#             assistant_id: Optional run ID
#             instructions: Assistant instructions
#             model: Model name
#             user_content: User message content
#             tools: List of tools for the assistant

#         Если указаны assistant_id и thread_id — используется существующий ассистент и поток.  
#         Если одного из параметров нет — недостающее создаётся автоматически.  

#         Если передан user_content, сообщение отправляется в поток, и запускается выполнение ассистента (run).  
#         Если user_content отсутствует — выполнение не инициируется, возвращаются только assistant_id и thread_id.  

#         Ответ в любом случае содержит:  
#         - assistant_id  
#         - thread_id  
#         - run_id (только если был запущен run)
        
#         """
#         url = f"{self.url}{RUN_ASSIST_CUSTOM_0525}"
#         data = {**self.data}

#         # Add optional parameters (добавляем опциональные параметры)
#         if thread_id:
#             data["thread_id"] = thread_id
#         if assistant_id:
#             data["assistant_id"] = assistant_id
#         if instructions:
#             data["instructions"] = instructions
#         if model:
#             data["model"] = model
#         if user_content:
#             data["user_content"] = user_content
#         if tools:
#             data["tools"] = json.dumps(tools, ensure_ascii=False)
            
#         return await self.assis_post(url, data)




# async def main():
#     assist = AssistOpenAI()
#     print(await assist.list_assist_oa())


# asyncio.run(main())