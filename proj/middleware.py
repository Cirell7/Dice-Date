# yourapp/middleware.py
from django.utils.deprecation import MiddlewareMixin

class OnboardingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Добавляем флаг в контекст всех шаблонов
        if hasattr(response, 'context_data') and response.context_data is not None:
            response.context_data['show_onboarding'] = request.session.get('new_user', False)
            
            # Убираем флаг после первого показа
            if request.session.get('new_user'):
                del request.session['new_user']
                
        return response