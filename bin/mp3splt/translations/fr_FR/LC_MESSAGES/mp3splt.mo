��    S      �  q   L             l  '     �
  �   �
  2   j      �  K   �  .   
  '  9     a  +   ~  �   �     l     x  I   �  F   �  b   !  :   �  �   �  �   �     d    e  &  z     �     �  +   �  .   �  #   (     L     g     u     �     �  $   �  %   �        *   4  <   _      �     �     �     �     �  0   �     ,  G   :  ;   �  &   �  9   �  (     ,   H  T   u  .   �     �  (     Z   ;  #   �  ;   �     �  =     "   S     v  5   �     �  2   �  =     2   K  8   ~  G   �  $   �  :   $  &   _  $   �  *   �  $   �  1   �  .   -  5   \  (   �  +   �     �     �  ~       �    �      �#  �   �#  N   �$  (   %  [   -%  J   �%  �  �%  -   Y'  1   �'  �   �'     �(     �(  A   �(  K   )  ]   ^)  /   �)  V  �)  d  C+  2  �,  K  �-  m  '/  "   �0     �0  <   �0  7   1  ,   ;1     h1     {1     �1  !   �1  -   �1  ;   �1  ;   72  +   s2  5   �2  T   �2  $   *3     O3     f3     ~3     �3  3   �3     �3  W   �3  M   L4  .   �4  B   �4  5   5  .   B5  }   q5  9   �5  %   )6  D   O6  w   �6  2   7  b   ?7     �7  X   �7  F   8     a8  <   z8     �8  =   �8  J   9  9   Y9  L   �9  H   �9  +   ):  F   U:  2   �:  +   �:  1   �:  +   -;  5   Y;  9   �;  @   �;  I   
<  D   T<  	   �<  J   �<     G           H   $                            2       *   <       -   M                  E   Q       &   6       )   =      D          #   3   S              7      5   +   J   K       N      4           8      @       %       "   ;   (   /   A          1   ?      !            >       0         '       
   P          .                F   R      I             	   :   B           O       C   L             9   ,          
  Search string: %s
 
 +-----------------------------------------------------------------------------+
 |NOTE: When you use cddb/cue, split files might be not very precise due to:|
 |1) Who extracts CD tracks might use "Remove silence" option. This means that |
 |   the large mp3 file is shorter than CD Total time. Never use this option.  |
 |2) Who burns CD might add extra pause seconds between tracks.  Never do it.  |
 |3) Encoders might add some padding frames so  that  file is longer than CD.  |
 |4) There are several entries of the same cd on CDDB, find the best for yours.|
 |   Usually you can find the correct splitpoints, so good luck!  |
 +-----------------------------------------------------------------------------+
 | TRY TO ADJUST SPLITS POINT WITH -a OPTION. Read man page for more details!  |
 +-----------------------------------------------------------------------------+
 
 split aborted. 
(other options)
 -T + TAGS_VERSION: for mp3 files, force output tags as version 1, 2 or 1 & 2.
      TAGS_VERSION can be 1, 2 or 12
      (default is to set the same version as the file to split) 
-- 'Enter' for more, 's' to split, 'c' to cancel: 
-- 's' to split, 'c' to cancel: 
All files have been split correctly. Visit http://mp3wrap.sourceforge.net! 
Getting file from %s on port %d using %s ...
 
OPTIONS (split mode options)
 -t + TIME: to split files every fixed time len. (TIME format same as above). 
 -c + file.cddb, file.cue or "query" or "query{album}". Get splitpoints and
      filenames from a .cddb or .cue file or from Internet ("query").
      Use -a to auto-adjust splitpoints. 
Please search something ... 
Searching from %s on port %d using %s ...
 
USAGE:
      mp3splt [OPTIONS] FILE1 [FILE2] ... [BEGIN_TIME] [TIME] ... [END_TIME]
      TIME FORMAT: min.sec[.0-99], even if minutes are over 59
                   (or EOF for End Of File).   Search: [    File "%s" created%s
  -A + AUDACITY_FILE: split with splitpoints from the audacity labels file  -E + CUE_FILE: export splitpoints to CUE file (use with -P if needed)  -P   Pretend to split: simulation of the process, without creating any
      files or directories  -S + SPLIT_NUMBER: split in SPLIT_NUMBER equal time files  -d + DIRNAME: to put all output files in the directory DIRNAME.
 -k   Consider input not seekable (slower). Default when input is STDIN (-).
 -O + TIME: Overlap split files with TIME (slower).  -m + M3U_FILE: Appends to the specified m3u file the split filenames.
 -f   Frame mode (mp3 only): process all frames. For higher precision and VBR.
 -a   Auto-Adjust splitpoints with silence detection. (Use -p for arguments)  -n   No Tag: does not write ID3v1 or vorbis comment. If you need clean files.
 -x   No Xing header: does not write the Xing header. Use with -n if you wish
      to concatenate the split files
 -N   Don't create the 'mp3splt.log' log file when using '-s'.  -q   Quiet mode: try not to prompt (if possible) and print less messages.
 -Q   Very quiet mode: don't print anything to stdout and no progress bar
       (also enables -q).
 -D   Debug mode: used to debug the program.

      Please read man page for complete documentation.
  -s   Silence detection: automatically find splitpoint. (Use -p for arguments)
 -w   Splits wrapped files created with Mp3Wrap or AlbumWrap.
 -l   Lists the tracks from file without extraction. (Only for wrapped mp3)
 -e   Error mode: split mp3 with sync error detection. (For concatenated mp3)  Average silence level: %.2f dB  Error: %s
  Freedb get type: %s , Site: %s , Port: %d
  Freedb search type: %s , Site: %s , Port: %d
  Pretending to split file '%s' ...
  Processing file '%s' ...
  Warning: %s
  creating "%s" (%d of %d)  preparing "%s" (%d of %d)  searching for sync errors... -- 'q' to select cd, Enter for more: -- 'q' to select cd, Enter for more:  -a option cannot be used with -i -s option cannot be used with -a, -i or -S CDDB QUERY. Insert album and artist informations to find cd. CommandLineToArgvW failed (oh !) List of found cd: List of found files:
 Please  Revision: %d
 S: %02d, Level: %.2f dB; scanning for silence... Select cd #:  THIS SOFTWARE COMES WITH ABSOLUTELY NO WARRANTY! USE AT YOUR OWN RISK!
 bad argument for -p option. No valid value was recognized ! bad gap argument. It will be ignored ! bad minimum silence length argument. It will be ignored ! bad offset argument. It will be ignored! bad threshold argument. It will be ignored ! bad time expression for the time split.
	Must be min.sec, read man page for details. bad tracknumber argument. It will be ignored ! cannot allocate memory ! cannot use '-o -' (STDOUT) with -m or -d cannot use -k option (or STDIN) with one of the following options: -S -s -w -l -e -i -a -p failed to allocate argv_utf8 memory found non digits characters in port ! (switched to default) freedb query format ambigous ! freedb web search not implemented yet ! (switched to default) multiple splitpoints with stdout ! no input filename(s). read man page for documentation or type 'mp3splt -h'. tags format ambiguous ! the -A option cannot be used with -t, -s, -i or -S the -N option must be used with silence detection (-s option) the -O option cannot be used with -w, -e, -l or -i the -Q option cannot be used with STDOUT output ('-o -') the -Q option cannot be used with interactive freedb query ('-c query') the -d option cannot be used with -i the -e option can only be used with -m, -f, -o, -d, -q, -Q the -l option can only be used with -q the -m option cannot be used with -i the -n option cannot be used with -i or -T the -o option cannot be used with -i the -p option cannot be used without -a, -s or -i the -t option cannot be used with -s, -i or -S the -w option can only be used with -m, -d, -q and -Q unknown get type ! (switched to default) unknown search type ! (switched to default) using using time mode with stdout ! Project-Id-Version: mp3splt-gtk
Report-Msgid-Bugs-To: io_fx@yahoo.fr
POT-Creation-Date: 2011-03-05 21:57+0100
PO-Revision-Date: 2011-02-22 00:08+0000
Last-Translator: peterpall <gunter@peterpall.de>
Language-Team: LANGUAGE <LL@li.org>
Language: fr_FR
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n > 1)
 
  Chaîne cherchée : %s
 
 +-----------------------------------------------------------------------------+
 NOTE: A l'utilisation de cddb/cue, les fichiers divisés peuvent ne pas être très précis à cause de :
  1) A l'extraction du CD, les pistes peuvent utiliser l'option "Supprimer le silence". Cela signifie
      que le temps du fichier mp3 est inférieur au temps total sur le CD. Ne jamais utiliser
      cette option.
  2) Celui qui grave le CD peut ajouter du silence entre les pistes. Ne jamais le faire.
  3) Les encodeurs peuvent ajouter des trames supplémentaires, ce qui rend le fichier plus
      long que sur le CD.
  4) Il existe plusieurs fichiers résultats CDDB pour le même CD. Trouvez le meilleur pour
      vos besoins. D'habitude, on peut trouver les points de coupure corrects.
 +-----------------------------------------------------------------------------+
    ESSAYEZ D'ADJUSTER LES POINTS AVEC L'OPTION -a.
    Lisez le manuel pour plus de détails !
 +-----------------------------------------------------------------------------+
 
 processus de division annulé. 
(autres options)
 -T + VERSION_TAGS : pour les fichiers mp3, forcer la version des tags
      comme 1, 2 ou 1 et 2. VERSION_TAGS peut être 1, 2 ou 12
      (par défaut: la même version que dans le fichier d'entrée) 
-- 'Entrée' pour voir plus de fichiers, 's' pour diviser, 'c' pour annuler : 
-- 's' pour diviser, 'c' pour annuler : 
Tous les fichiers ont été divisés avec succès. Visitez http://mp3wrap.sourceforge.net! 
Récupération du fichier à partir de %s et le port %d utilisant %s ...
 
OPTIONS (options du mode de division)
 -t + TEMPS : pour diviser le fichier en plusieurs pistes de même taille (taille égale à TEMPS)
 -c + fichier.cddb, fichier.cue ou "query" ou "query{album}". Récupérer les
      points de coupure à partir d'un fichier .cddb ou .cue ou à partir d'internet ("query").
      Utiliser -a pour ajuster les points de coupure en fonction du silence. 
S'il vous plaît, cherchez quelque chose ... 
Recherche sur %s et le port %d utilisant %s ...
 
UTILISATION :
      mp3splt [OPTIONS] FICHIER1 [FICHIER2] ... [TEMPS_DEBUT] [TEMPS] ... [TEMPS_FIN]
      Format du TEMPS: min.sec[.0-99], même si les minutes sont supérieurs à 59
                    (ou EOF pour la fin du fichier).   Chercher : [    Fichier "%s" créé%s
  -A + FICHIER_AUDACITY : division à partir de marqueurs audacity  -E + FICHIER_CUE : exporter les points vers un fichier CUE (voir aussi -P)  -P   Simulation du processus de division, sans créer des fichiers ou
      des répertoires  -S + NOMBRE : diviser en NOMBRE morceaux egaux  -d + REPERTOIRE : créer les fichiers dans le répertoire REPERTOIRE.
 -k + Considérer l'entrée comme un flux sur lequel on ne peut pas
      changer la position (plus lent). Par défaut quand l'entrée est le flux standard
      d'entrée (STDIN, '-').
 -O + TEMPS : Chevaucher les fichiers créés sur un intervalle de TEMPS (plus lent).  -m + FICHIER_M3U : ajoute à la fin du fichier FICHIER_M3U les noms des
      fichiers obtenus.
 -f   Mode 'frame' (seulement mp3) : parcourir toutes les 'frames'. Pour une meilleure
      précision et fichiers VBR (taux d'échantillonnage variable)
 -a   Ajustement des points de coupure avec recherche du silence.
      (Utiliser -p pour les arguments)  -n   Pas de tag : n'écrit pas de tag ID3 ou vorbis dans les fichiers crées.
 -x   Pas d'entête Xing : n'écrit pas l'entête Xing. Utiliser avec -n si besoin de concaténer
      les fichiers divisés.
 -N   Ne pas créer le fichier de log 'mp3splt.log' avec les points desilence quand -s est utilisé.  -q   Mode silencieux: affiche moins de messages et moins d'intéraction utilisateur
 -Q   Mode très silencieux: n'affiche rien sur la sortie standard et pas de barre de
      progression (active l'option -q).
 -D   Mode 'débogage' : utilisé pour débogguer le programme.

      Lire le manuel pour une documentation complète.
  -s   Trouver les points de coupure automatiquement en recherchant le silence
      (Utiliser -p pour les arguments)
 -w   Division 'wrap' : diviser les fichiers crées avec Mp3Wrap ou AlbumWrap.
 -l   Lister les pistes du fichier 'wrap' sans extraction.
 -e   Mode de division par recherche des erreurs de synchronisation (pour les fichiers mp3
      concaténés)  Niveau de silence moyen : %.2f dB  Erreur : %s
  Type de récupération freedb : %s , Site : %s , Port : %d
  Type de recherche freedb : %s , Site : %s , Port : %d
  Simulation de division du fichier '%s' ...
  Fichier '%s' ...
  Attention : %s
  création de "%s" (%d sur %d)  préparation de "%s" (%d sur %d)  recherche des erreurs de synchronisation ... -- 'q' pour sélectionner un CD, Entrée pour plus de CDs : -- 'q' pour sélectionner un CD, Entrée pour plus de CDs : l'option -a ne peut être utilisée avec -i l'option -s ne peut être utilisée avec -a, -i ou -S RECHERCHE CDDB. Entrez des informations sur l'album et l'artiste pour trouver un CD. CommandLineToArgvW a échoué (oh !) Liste de CD trouvés : Liste de CD trouvés :
 S'il vous plaît  Révision : %d
 S : %02d, Niveau : %.2f dB; recherche du silence... Sélectionnez le CD numéro # : CE PROGRAMME EST FOURNI SANS AUCUNE GARANTIE ! UTILISEZ-LE SOUS VOTRE RESPONSABILITE !
 mauvais argument pour l'option -p. Aucune valeur valide n'a été réconnue ! mauvais argument pour l'écart. Sera ignoré ! mauvais argument pour la taille minimum du silence. Sera ignoré ! mauvais argument pour la compensation. Sera ignoré ! mauvais argument pour le seuil. Sera ignoré ! mauvaise valeur pour la division en plusieurs pistes de même taille.
	Doit être min.sec, lisez le manuel pour les détails. mauvais argument pour le nombre de pistes. Sera ignoré ! impossible d'allouer de la mémoire ! impossible d'utiliser '-o -' (flux de sortie standard) avec -m ou -d impossible d'utiliser l'option -k (ou flux d'entrée standard) avec une des options suivantes : -S -s -w -l -e -i -a -p impossible d'allouer de la mémoire pour argv_utf8 détection des caractères autre que des chiffres dans le port ! (utilisation du port par défaut) format freedb 'query' ambigu ! recherche web freedb pas encore implementée ! (utilisation de la recherche par défaut) plusieurs points de coupure avec le flux de sortie standard (stdout) ! aucun fichier d'entrée. lisez le manuel pour la documentation ou tapez 'mp3splt -h'. format des tags ambigu ! l'option -A ne peut pas être utilisée avec -t, -s, -i ou -S l'option -N doit être utilisée avec la détection de silence (option -s) l'option -O ne peut être utilisée avec -w, -e, -l ou -i l'option -Q ne peut être utilisée avec le flux standard de sortie ('-o -') l'option -Q ne peut être utilisée avec la requête freedb ('-c query') l'option -d ne peut être utilisée avec -i l'option -e peut seulement être utilisée avec -m, -f, -o, -d, -q, -Q l'option -l peut seulement être utilisée avec -q l'option -m ne peut être utilisée avec -i l'option -n ne peut être utilisée avec -i ou -T l'option -o ne peut être utilisée sans -i l'option -p ne peut être utilisée sans -a, -s ou -i l'option -t ne peut pas être utilisée avec -s, -i ou -S l'option -w peut seulement être utilisée avec -m, -d, -q et -Q type de récupération freedb inconnu ! (utilisation du type par défaut) type de recherche freedb inconnu ! (utilisation du type par défaut) utilisant utilisation du mode de division 'temps' avec la sortie standard (stdout) ! 