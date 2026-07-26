import 'dart:convert';
import 'dart:io';

class NetSecureProApiService {
  final String _baseUrl = 'http://127.0.0';

  Future<Map<String, dynamic>> analyserFluxReseau(String texteAAnalyser) async {
    final HttpClient client = HttpClient();
    try {
      final HttpClientRequest request = await client.postUrl(Uri.parse(_baseUrl));
      request.headers.set(HttpHeaders.contentTypeHeader, 'application/json; charset=utf-8');
      
      final Map<String, String> payload = {'texte': texteAAnalyser};
      request.write(jsonEncode(payload));
      
      final HttpClientResponse response = await request.close();
      final String responseBody = await response.transform(utf8.decoder).join();
      
      if (response.statusCode == 200) {
        return jsonDecode(responseBody) as Map<String, dynamic>;
      } else if (response.statusCode == 429) {
        return {
          'success': false,
          'security_status': 'REJETÉ',
          'summary': 'Alerte Trafic : Rejeté par le Rate Limiter local [429].'
        };
      } else {
        return {
          'success': false,
          'security_status': 'ERREUR_NOYAU',
          'summary': 'Erreur de routage de l\'API locale : ${response.statusCode}'
        };
      }
    } catch (e) {
      return {
        'success': false,
        'security_status': 'DÉCONNECTÉ',
        'summary': 'Serveur ia_zer0 introuvable. Exécutez app_ia_production.py.'
      };
    } finally {
      client.close();
    }
  }
}
