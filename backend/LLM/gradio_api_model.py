from gradio_client import Client

# Class for model with gradio api (only sync available) 
class GradioModel:
    def __init__(self, model) -> None:
        self.client = Client(model)
        
        pass
    
    def get_prediction(self, text:str):
        result = self.client.predict(
                query=f"{text}",
                #history not working 
                history=[],
                system="You are a helpful assistant.",
                api_name="/model_chat"
            )
        return result[1][0][1]

