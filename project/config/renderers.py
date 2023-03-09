from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        response = {
            "status": "success",
            "code": status_code,
            "data": data,
            "message": None,
        }
        try:
            for i in response["data"].get("errors"):
                attr = i.get("attr")
                if attr == None:
                    if i["code"] == "permission_denied":
                        i["detail"] = i["code"]
                    else:
                        i["detail"] = i["detail"].replace(" ", "_").lower()
                else:
                    if isinstance(i["code"], str):
                        if i["code"] != "error":
                            i["detail"] = f"{attr}_" + i["code"]
                del i["attr"], i["code"]
        except (TypeError, AttributeError):
            pass

        if not str(status_code).startswith("2"):
            response["status"] = "error"
            response["data"] = None
            try:
                response["message"] = data["detail"]
            except KeyError:
                response["data"] = data

        return super(CustomRenderer, self).render(
            response, accepted_media_type, renderer_context
        )
