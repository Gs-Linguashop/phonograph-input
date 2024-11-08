# 諧聲聲符兼容輸入

這是一款實現正常輸入時也可以選擇[諧聲聲符](https://github.com/Gs-Linguashop/sino-phonographics.git)書寫的輸入法工具。這款工具基於[RIME輸入法](https://rime.im)，可以把普通的RIME字典轉換成兼容諧聲聲符輸入的字典。

## 什麼是諧聲聲符文字？

諧聲聲符文字是漢字中形聲字的上千個表音偏旁構成的表音文字。用諧聲書寫中文時，可以只保留形聲字的表音部分，自由地省略不影響閱讀的形聲字表意部分，從而讓漢字的使用更表音化、簡明和自由。

匕如見在這段文子就是用皆殸勺方式書舄勺。這重書舄習貫是對𦰩子向表音化癶展的一次尚式。其于見代𦰩五中多子司匕列曾加、音即囪量下夅等寺占，皆殸文子可能匕專充𦰩子更啇合書舄見代𦰩五。

關於諧聲文字，在[這裏](https://github.com/Gs-Linguashop/sino-phonographics.git)有更詳細的描述。

## 什麼是RIME輸入法？

RIME輸入法是一款免費多平台個性化定制輸入法的工具。它讓用戶可以自由地定義和設計漢字輸入方案。本項目就是通過RIME輸入法實現的。

關於RIME輸入法，在[這裏](https://rime.im)有更詳細的描述。在[這裏](https://github.com/rime/home/wiki/RimeWithSchemata)可以找到詳細的使用說明。

### 如何在RIME輸入法中部署諧聲聲符兼容輸入？

本諧聲兼容輸入是一款將已有的RIME輸入方案轉換成諧聲兼容的輸入方案的工具，所以您需要先安裝RIME輸入法，並在其中部署一款已有的輸入方案（本項目以[朙月拼音](https://github.com/rime/rime-luna-pinyin)爲例）。您可以在這裏了解並熟悉RIME輸入法。

將您選用的輸入方案的字典文件的字頭複製出來，新建一個字頭文件。我們將以此文件作爲諧聲兼容字典文件的新字頭。

修改字頭文件中的`name`部分，取一個新的字典`name`，與原來的`name`區分。

修改字頭文件中的`use_preset_vocabulary`部分爲`use_preset_vocabulary: false`。

在`main.py`中修改字頭文件路徑、原字典文件路徑、原字典文件中正文開始的行號、輸出字典文件路徑等信息。

如果需要，您可以在`src`中調整諧聲兼容輸入的兼容內容。這裏預先給出的內容基於[諧聲聲符文字項目](https://github.com/Gs-Linguashop/sino-phonographics.git)中對應的文件。

運行`main.py`。

將得到的新字典文件部署到RIME中。您需要一下操作。

將得到的新字典文件複製到RIME設置文件夾中。

參考RIME的說明，將新字典文件作爲用戶自定義字典文件導入。確保部署時選用`use_preset_vocabulary: false`。

把原輸入方案schema文件中所用的字典更改爲新字典的名稱。

如果schema文件中的grammar-language部分使用了包含“essay”字樣的語法，那麼刪除這個語法設置。

部署RIME。您應該可以正常使用諧聲兼容的輸入了。