"""Handler for selecting and running editor features"""

from typing import Any, Union

from . import (
    helper,
    user_input_handler,
    config_manager,
)
from .edits import basic, cats, gamototo, levels, other, save_management


def fix_elsewhere_old(save_stats: dict[str, Any]) -> dict[str, Any]:
    """Fix the elsewhere error using 2 save files"""

    main_token = save_stats["token"]
    main_iq = save_stats["inquiry_code"]
    input(
        "오류가 없고 밴되지 않은 현재 게임 내 로드된 저장 파일을 선택하세요.\n엔터를 눌러 계속:"
    )
    new_path = helper.select_file(
        "세이브 파일 선택",
        helper.get_save_file_filetype(),
        helper.get_save_path(),
    )
    if not new_path:
        print("세이브 파일을 선택해주세요")
        return save_stats

    data = helper.load_save_file(new_path)
    new_stats = data["save_stats"]
    new_token = new_stats["token"]
    new_iq = new_stats["inquiry_code"]
    save_stats["token"] = new_token
    save_stats["inquiry_code"] = new_iq

    helper.colored_text(f"문의 코드 교체됨: &{main_iq}& -> &{new_iq}&")
    helper.colored_text(f"토큰 교체됨: &{main_token}& -> &{new_token}&")
    return save_stats


FEATURES: dict[str, Any] = {
    "세이브 관리": {
        "세이브 저장" : save_management.save.save_save,
        "세이브 저장 및 데이터 업로드(기종변경 코드 받기)": save_management.server_upload.save_and_upload,
        "세이브 파일에 저장": save_management.save.save,
        "세이브 데이터 게임에 인젝팅 (게임 다시시작 안함)": save_management.save.save_and_push,
        "세이브 데이터 게임에 인젝팅 (게임 다시시작 함)": save_management.save.save_and_push_rerun,
        "세이브 데이터 json으로 내보내기": save_management.other.export,
        "세이브 데이터 공장초기화": save_management.other.clear_data,
        "추적되는 밴 가능성이 있는 아이템 처리(업로드 시 자동 실행)": save_management.server_upload.upload_metadata,
        "세이브 데이터 로드" : save_management.load.select,
        #"Manage Presets": preset_handler.preset_manager,
    },
    "아이템": {
        "통조림": basic.basic_items.edit_cat_food,
        "경험치": basic.basic_items.edit_xp,
        "티켓": {
            "냥코 티켓": basic.basic_items.edit_normal_tickets,
            "레어 티켓": basic.basic_items.edit_rare_tickets,
            "플레티넘 티켓": basic.basic_items.edit_platinum_tickets,
            "플레티넘 조각": basic.basic_items.edit_platinum_shards,
            "레전드 티켓": basic.basic_items.edit_legend_tickets,
        },
        "NP": basic.basic_items.edit_np,
        "리더쉽": basic.basic_items.edit_leadership,
        "배틀 아이템": basic.basic_items.edit_battle_items,
        "캣츠아이": basic.catseyes.edit_catseyes,
        "개다래 / 수석": basic.catfruit.edit_catfruit,
        "본능구슬": basic.talent_orbs.edit_talent_orbs,
        "고양이 드링크": basic.basic_items.edit_catamins,
        "항목 구성표(밴할 수 없는 항목을 얻을 수 있음)": other.scheme_item.edit_scheme_data,
    },
    "가마토토 / 오토토": {
        "오토토 조수": basic.basic_items.edit_engineers,
        "성 재료": basic.basic_items.edit_base_materials,
        "고양이 드링크": basic.basic_items.edit_catamins,
        "가마토토 경험치 / 레벨": gamototo.gamatoto_xp.edit_gamatoto_xp,
        "오토토 성 대포": gamototo.ototo_cat_cannon.edit_cat_cannon,
        "가마토토 대원": gamototo.helpers.edit_helpers,
        "가마토토가 게임오류 발생시키는 것 고치기": gamototo.fix_gamatoto.fix_gamatoto,
    },
    "캐릭터 / 본능 / 특능": {
        "캐릭터 얻기 / 삭제": {
            "캐릭터 얻기": cats.get_remove_cats.get_cat,
            "캐릭터 삭제": cats.get_remove_cats.remove_cats,
        },
        "캐릭터 레벨업": cats.upgrade_cats.upgrade_cats,
        "캐릭터 3단진화": {
            "3단진화 얻기": cats.evolve_cats.get_evolve,
            "3단진화 삭제": cats.evolve_cats.remove_evolve,
            "강제 3단진화 하기 (3진 형태가 없는 캐릭터의 경우 오류 발생 가능)": cats.evolve_cats.get_evolve_forced,
        },
        "본능": {
            "선택한 각 캐릭터의 본능을 개별적으로 설정": cats.talents.edit_talents_individual,
            "선택된 모든 캐릭터들의 본능 최대 / 제거": cats.talents.max_all_talents,
        },
        "캐릭터 가이드": {
            "캐릭터 가이드 얻기 (통조림 안줌)": cats.clear_cat_guide.collect_cat_guide,
            "캐릭터 가이드 삭제": cats.clear_cat_guide.remove_cat_guide,
        },
        '스테이지 보상 캐릭터': cats.chara_drop.get_character_drops,
        "본능 업그레이드": cats.upgrade_blue.upgrade_blue,
    },
    "스테이지 / 보물": {
        "스토리편": {
            "선택한 모든 챕터의 모든 챕터에서 각 스테이지 클리어": levels.main_story.clear_all,
            "선택한 각 챕터의 모든 챕터에서 각 스테이지 클리어": levels.main_story.clear_each,
        },
        "보물": {
            "보물 그룹별로 세팅": levels.treasures.treasure_groups,
            "특정 스테이지와 특정 보물 각각 설정": levels.treasures.specific_stages,
            "모두 한번에 설정": levels.treasures.specific_stages_all_chapters,
        },
        "좀비 스테이지": levels.outbreaks.edit_outbreaks,
        "이벤트 스테이지": levels.event_stages.event_stages,
        "구 레전드": levels.event_stages.stories_of_legend,
        "신 레전드": levels.uncanny.edit_uncanny,
        "마계편": levels.aku.edit_aku,
        "마계편 잠금해제s": levels.unlock_aku_realm.unlock_aku_realm,
        "강습": levels.gauntlet.edit_gauntlet,
        "콜라보 강습": levels.gauntlet.edit_collab_gauntlet,
        "탑": levels.towers.edit_tower,
        "초수 스테이지": levels.behemoth_culling.edit_behemoth_culling,
        "미래편 시간 점수": levels.itf_timed_scores.timed_scores,
        "챌린지 배틀 점수": basic.basic_items.edit_challenge_battle,
        "튜토리얼 클리어": levels.clear_tutorial.clear_tutorial,
        "냥코 도장": basic.basic_items.edit_dojo_score,
        "발굴 스테이지": levels.enigma_stages.edit_enigma_stages,
        "필리버스터 스테이지 재클리어 가능하게 만들기" : levels.allow_filibuster_clearing.allow_filibuster_clearing,
        "전설의 퀘스트": levels.legend_quest.edit_legend_quest,
    },
    "문의코드 / 토큰 / 계정": {
        "문의코드": basic.basic_items.edit_inquiry_code,
        "토큰": basic.basic_items.edit_token,
        "에러 고치기 / 밴 풀기": other.fix_elsewhere.fix_elsewhere,
        "에러 고치기 / 밴 풀기 (세이브 파일 2개 필요)": fix_elsewhere_old,
        "새 문의코드와 토큰 생성": other.create_new_account.create_new_account,
    },
    "기타": {
        "레어 뽑기 시드": basic.basic_items.edit_rare_gacha_seed,
        "슬롯 잠금해제": basic.basic_items.edit_unlocked_slots,
        "리스타트 팩": basic.basic_items.edit_restart_pack,
        "냥코 메달": other.meow_medals.medals,
        "플레이타임": other.play_time.edit_play_time,
        "적 가이드": other.unlock_enemy_guide.enemy_guide,
        "미션": other.missions.edit_missions,
        "일반 티켓 최대 거래 진행률(밴할 수 없는 레어 티켓 허용)": other.trade_progress.set_trade_progress,
        "골드패스": other.get_gold_pass.get_gold_pass,
        "유저랭크 보상 모두 처리(아이템 안줌)": other.claim_user_rank_rewards.edit_rewards,
        "냥코 사당 레벨": other.cat_shrine.edit_shrine_xp,
    },
    "오류수정/기타": {
        "시간 오류 고치기" : other.fix_time_issues.fix_time_issues,
        "슬롯 잠금해제": other.unlock_equip_menu.unlock_equip,
        "튜토리얼 클리어": levels.clear_tutorial.clear_tutorial,
        "다른 곳 오류 수정 / 계정 밴 해제": other.fix_elsewhere.fix_elsewhere,
        "다른 곳 오류 수정 / 계정 밴 해제 (세이브 파일 2개 필요)": fix_elsewhere_old,
        "가마토토 고치기": gamototo.fix_gamatoto.fix_gamatoto,
    },
    "에딧 설정 (함부로 건드리면 오류남)": {
        "Edit DEFAULT_COUNTRY_CODE": config_manager.edit_default_gv,
        "Edit DEFAULT_SAVE_PATH": config_manager.edit_default_save_file_path,
        "Edit FIXED_SAVE_PATH": config_manager.edit_fixed_save_path,
        "Edit EDITOR settings": config_manager.edit_editor_settings,
        "Edit START_UP settings": config_manager.edit_start_up_settings,
        "Edit SAVE_CHANGES settings": config_manager.edit_save_changes_settings,
        "Edit SERVER settings": config_manager.edit_server_settings,
        "Edit config path": config_manager.edit_config_path,
    },
    "에디터 종료": helper.exit_check_changes,
}


def get_feature(
    selected_features: Any, search_string: str, results: dict[str, Any]
) -> dict[str, Any]:
    """Search for a feature if the feature name contains the search string"""

    for feature in selected_features:
        feature_data = selected_features[feature]
        if isinstance(feature_data, dict):
            feature_data = get_feature(feature_data, search_string, results)
        if search_string.lower().replace(" ", "") in feature.lower().replace(" ", ""):
            results[feature] = selected_features[feature]
    return results


def show_options(
    save_stats: dict[str, Any], features_to_use: dict[str, Any]
) -> dict[str, Any]:
    """Allow the user to either enter a feature number or a feature name, and get the features that match"""

    if (
        not config_manager.get_config_value_category("EDITOR", "SHOW_CATEGORIES")
        and FEATURES == features_to_use
    ):
        user_input = ""
    else:
        prompt = (
            "에딧할 것을 선택하세요."
        )
        if config_manager.get_config_value_category(
            "EDITOR", "SHOW_FEATURE_SELECT_EXPLANATION"
        ):
            prompt += "\n숫자를 입력하여 기능을 실행하거나 단어를 입력하여 해당 기능을 검색할 수 있습니다(예: catfood를 입력하면 Cat Food 기능이 실행되고 티켓을 입력하면 티켓을 편집하는 모든 기능이 표시됨)\nEnter를 누르면 모든 기능 목록이 표시됨"
        user_input = user_input_handler.colored_input(f"{prompt}:\n")
    user_int = helper.check_int(user_input)
    results = []
    if user_int is None:
        results = get_feature(features_to_use, user_input, {})
    else:
        if user_int < 1 or user_int > len(features_to_use) + 1:
            helper.colored_text("범위을 벗어남", helper.RED)
            return show_options(save_stats, features_to_use)
        if FEATURES != features_to_use:
            if user_int - 2 < 0:
                return menu(save_stats)
            results = features_to_use[list(features_to_use)[user_int - 2]]
        else:
            results = features_to_use[list(features_to_use)[user_int - 1]]
    if not isinstance(results, dict):
        save_stats_return = results(save_stats)
        if save_stats_return is None:
            return save_stats
        return save_stats_return
    if len(results) == 0:
        helper.colored_text("검색되지 않음.", helper.RED)
        return menu(save_stats)
    if len(results) == 1 and isinstance(list(results.values())[0], dict):
        results = results[list(results)[0]]
    if len(results) == 1:
        save_stats_return = results[list(results)[0]](save_stats)
        if save_stats_return is None:
            return save_stats
        return save_stats_return

    helper.colored_list(["뒤로가기"] + list(results))
    return show_options(save_stats, results)


def menu(
    save_stats: dict[str, Any], path_save: Union[str, None] = None
) -> dict[str, Any]:
    """Show the menu and allow the user to select a feature to edit"""

    if path_save:
        helper.set_save_path(path_save)
    if config_manager.get_config_value_category("EDITOR", "SHOW_CATEGORIES"):
        helper.colored_list(list(FEATURES))
    save_stats = show_options(save_stats, FEATURES)

    return save_stats
