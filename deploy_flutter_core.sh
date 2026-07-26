#!/bin/bash
set -e

echo -e "\033[1;34m[*] Initialisation du déploiement mobile NetSecurePro IA v9 [NANS Core]...\033[0m"

# 1. Création du fichier de service de l'API souveraine
echo -e "[+] Génération du module de service réseau (api_service.dart)..."
cat << 'INNER_EOF' > api_service.dart
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
INNER_EOF

# 2. Création de l'interface utilisateur unifiée Cyberpunk
echo -e "[+] Fusion avec l'interface graphique mobile (main.dart)..."
cat << 'INNER_EOF' > main.dart
import 'package:flutter/material.dart';
import 'api_service.dart';

void main() {
  runApp(const NetSecureProApp());
}

class NetSecureProApp extends StatelessWidget {
  const NetSecureProApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'NetSecurePro IA v9',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xff0a0e14),
        primaryColor: const Color(0xff00ff9f),
        textSelectionTheme: const TextSelectionThemeData(
          cursorColor: Color(0xff00ff9f),
        ),
      ),
      home: const ConsoleAutonomeScreen(),
    );
  }
}

class ConsoleAutonomeScreen extends StatefulWidget {
  const ConsoleAutonomeScreen({super.key});

  @override
  State<ConsoleAutonomeScreen> createState() => _ConsoleAutonomeScreenState();
}

class _ConsoleAutonomeScreenState extends State<ConsoleAutonomeScreen> {
  final TextEditingController _fluxController = TextEditingController();
  final NetSecureProApiService _apiService = NetSecureProApiService();
  bool _isLoading = false;
  String _resultLog = "Console prête. En attente de l'analyse du flux...";

  void _lancerAnalyse() async {
    final String input = _fluxController.text.trim();
    if (input.isEmpty) return;

    setState(() {
      _isLoading = true;
      _resultLog = ">> INITIALISATION DE L'AUDIT SOUVERAIN V-IA22...\n>> REQUÊTE EXPÉDIÉE AU NOYAU LOCAL...";
    });

    final resultat = await _apiService.analyserFluxReseau(input);

    setState(() {
      _isLoading = false;
      if (resultat['success'] == true) {
        _resultLog = "--- RÉPONSE CONSOLE AUTONOME ---\n"
            "Session ID : ${resultat['session_id']}\n"
            "Document Type : ${resultat['document_type']}\n"
            "Statut Sécurité : ${resultat['security_status']}\n"
            "Synthèse : ${resultat['summary']}";
      } else {
        _resultLog = "--- ALERTE INFRASTRUCTURE ---\n"
            "Statut : ${resultat['security_status']}\n"
            "Détails : ${resultat['summary']}";
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          '⚡ NetSecurePro IA v9 – Console Autonome',
          style: TextStyle(
            color: Color(0xff00ff9f),
            fontWeight: FontWeight.bold,
            fontSize: 16,
            letterSpacing: 1.1,
          ),
        ),
        backgroundColor: const Color(0xff0a0e14),
        elevation: 0,
        centerTitle: true,
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(1.0),
          child: Container(color: const Color(0xff00ff9f), height: 1.0),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: 10),
            // Zone d'entrée de texte conforme à l'interface originale
            TextField(
              controller: _fluxController,
              maxLines: 4,
              style: const TextStyle(color: Colors.white, fontFamily: 'RobotoMono'),
              decoration: InputDecoration(
                hintText: 'Entrez le texte du document...',
                hintStyle: const TextStyle(color: Colors.grey),
                enabledBorder: const OutlineInputBorder(
                  borderSide: BorderSide(color: Color(0xff121824), width: 2),
                ),
                focusedBorder: const OutlineInputBorder(
                  borderSide: BorderSide(color: Color(0xff00ff9f), width: 2),
                ),
                filled: true,
                fillColor: const Color(0xff121824),
              ),
            ),
            const SizedBox(height: 16),
            // Bouton Analyser le Flux
            ElevatedButton(
              onPressed: _isLoading ? null : _lancerAnalyse,
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xff38bdf8), // Bleu conforme à la capture v9
                foregroundColor: Colors.black,
                padding: const EdgeInsets.vertical(14),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(4),
                ),
              ),
              child: _isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        valueColor: AlwaysStoppedAnimation<Color>(Colors.black),
                      ),
                    )
                  : const Text(
                      'Analyser le Flux',
                      style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                    ),
            ),
            const SizedBox(height: 24),
            // Console de rendu des logs JSON / Réponses du serveur
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xff0f172a),
                borderRadius: BorderRadius.circular(4),
                border: Border.all(color: const Color(0xff1e293b), width: 1.5),
              ),
              child: SelectableText(
                _resultLog,
                style: const TextStyle(
                  fontFamily: 'RobotoMono',
                  fontSize: 13,
                  color: Color(0xffcbd5e1),
                  height: 1.5,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
INNER_EOF

print_border() {
    echo "====================================================================="
}

print_border
echo -e "📱 ARCHITECTURE INTERCONNECTÉE SCELLÉE : main.dart & api_service.dart"
echo -e "Statut du Front-End Mobile : PRÊT POUR INJECTION REQUÊTES"
print_border
